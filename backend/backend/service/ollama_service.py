"""Local-model client backed by Ollama's HTTP API.

The pipeline never depends on the LLM succeeding — every method has a
deterministic fallback so a fresh clone (or a hiccupping model) still
produces a valid assessment.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config import settings, BACKEND_ROOT
from constants import BLOOM_LEVELS, BLOOM_MARKS, DIFFICULTY_LEVELS, QUESTION_TYPES

logger = logging.getLogger(__name__)


PROMPTS_DIR = BACKEND_ROOT / "prompts"


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


CLASSIFY_PROMPT = _load_prompt("classify_prompt.txt")
GENERATE_PROMPT = _load_prompt("generate_prompt.txt")
ANSWER_PROMPT = _load_prompt("answer_prompt.txt")


class OllamaService:
    def health(self) -> bool:
        request = Request(f"{settings.ollama_url.rstrip('/')}/api/tags", method="GET")
        try:
            with urlopen(request, timeout=5) as response:
                return 200 <= response.status < 300
        except (HTTPError, URLError, TimeoutError):
            return False

    def _generate_json(self, prompt: str) -> dict | None:
        payload = {
            "model": settings.ollama_model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.4, "top_p": 0.9},
        }
        request = Request(
            f"{settings.ollama_url.rstrip('/')}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=settings.ollama_timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
            raw = body.get("response", "").strip()
            return json.loads(raw) if raw else None
        except (HTTPError, URLError, TimeoutError, KeyError, json.JSONDecodeError):
            logger.warning("Ollama call failed; using fallback.", exc_info=True)
            return None

    # ------------------------------------------------------------------ classify

    def classify_many(self, questions: list[dict], learning_outcomes: list[str], grade: str) -> list[dict]:
        """Batched classification: chunks of ``ollama_classify_batch_size``."""
        if not questions:
            return []
        chunk_size = max(1, settings.ollama_classify_batch_size)
        results: list[dict | None] = [None] * len(questions)
        for start in range(0, len(questions), chunk_size):
            chunk = questions[start : start + chunk_size]
            chunk_results = self._classify_chunk(chunk, learning_outcomes, grade)
            for offset, item in enumerate(chunk_results):
                results[start + offset] = item
        return [
            self._validate_classification(entry, question, learning_outcomes)
            for entry, question in zip(results, questions)
        ]

    def _classify_chunk(
        self, chunk: list[dict], learning_outcomes: list[str], grade: str,
    ) -> list[dict | None]:
        prompt = CLASSIFY_PROMPT.format(
            grade=grade,
            learning_outcomes_json=json.dumps(learning_outcomes),
            question_types_json=json.dumps(QUESTION_TYPES),
            questions_json=json.dumps(
                [{"index": index, "question": item.get("question", "")} for index, item in enumerate(chunk)]
            ),
        )
        result = self._generate_json(prompt) or {}
        by_index: dict[int, dict] = {}
        for classification in result.get("classifications", []) or []:
            if isinstance(classification, dict) and isinstance(classification.get("index"), int):
                by_index[classification["index"]] = classification
        return [by_index.get(index) for index in range(len(chunk))]

    # ------------------------------------------------------------------ generate

    def generate(
        self, requirement: dict, context: dict, teacher_prompt: str | None = None
    ) -> dict | None:
        prompt = GENERATE_PROMPT.format(
            grade=context.get("grade", "middle school"),
            chapter_name=context.get("chapterName", "the topic"),
            learning_outcome=requirement["learningOutcome"],
            difficulty=requirement["difficulty"],
            bloom_level=requirement["bloomLevel"],
            question_type=requirement["questionType"],
            marks=requirement["marks"],
            teacher_prompt=(teacher_prompt or "").strip(),
        )
        generated = self._generate_json(prompt)
        if not generated or not generated.get("question") or not generated.get("answer"):
            return None
        return {
            **generated,
            "difficulty": requirement["difficulty"],
            "bloomLevel": requirement["bloomLevel"],
            "questionType": requirement["questionType"],
            "marks": requirement["marks"],
            "learningOutcomes": [requirement["learningOutcome"]],
        }

    def regenerate_answer(
        self, question_text: str, learning_outcomes: list[str], grade: str, teacher_prompt: str | None
    ) -> str | None:
        prompt = ANSWER_PROMPT.format(
            grade=grade,
            learning_outcomes_json=json.dumps(learning_outcomes),
            question=question_text,
            teacher_prompt=(teacher_prompt or "").strip(),
        )
        result = self._generate_json(prompt)
        if not result:
            return None
        answer = result.get("answer")
        return answer.strip() if isinstance(answer, str) and answer.strip() else None

    # -------------------------------------------------------------- validation

    def _validate_classification(
        self, result: dict | None, question: dict, outcomes: list[str]
    ) -> dict:
        text = question.get("question", "") or ""
        options = question.get("options", []) or []
        if result is None:
            result = self._heuristic_classification(text, options, outcomes)

        difficulty = result.get("difficulty") if result.get("difficulty") in DIFFICULTY_LEVELS else "Medium"
        bloom = result.get("bloomLevel") if result.get("bloomLevel") in BLOOM_LEVELS else "Understand"
        question_type = result.get("questionType") if result.get("questionType") in QUESTION_TYPES else self._infer_type(text, options)

        matched_outcomes = [o for o in (result.get("learningOutcomes") or []) if o in outcomes]
        if not matched_outcomes:
            matched_outcomes = self._heuristic_outcome(text, outcomes)

        try:
            marks = int(result.get("marks", BLOOM_MARKS[bloom]))
        except (TypeError, ValueError):
            marks = BLOOM_MARKS[bloom]

        return {
            **question,
            "difficulty": difficulty,
            "bloomLevel": bloom,
            "questionType": question_type,
            "learningOutcomes": matched_outcomes,
            "marks": max(1, min(20, marks)),
        }

    def _heuristic_classification(self, text: str, options: list[str], outcomes: list[str]) -> dict:
        question_type = self._infer_type(text, options)
        bloom = self._infer_bloom(text, question_type)
        return {
            "difficulty": self._infer_difficulty(text, bloom),
            "bloomLevel": bloom,
            "questionType": question_type,
            "learningOutcomes": self._heuristic_outcome(text, outcomes),
            "marks": BLOOM_MARKS[bloom],
        }

    def _infer_type(self, text: str, options: list[str]) -> str:
        lower_opts = {str(item).strip().lower() for item in options}
        if lower_opts == {"true", "false"}:
            return "True / False"
        if len(options) >= 3:
            return "MCQ"
        if "____" in text or "fill in the blank" in text.lower():
            return "Fill in the Blank"
        long_signals = ("explain", "describe", "compare", "analyse", "analyze", "discuss")
        if len(text) > 140 or any(signal in text.lower() for signal in long_signals):
            return "Long Answer"
        return "Short Answer"

    def _infer_bloom(self, text: str, question_type: str) -> str:
        lower = text.lower()
        if any(word in lower for word in ("analyse", "analyze", "compare", "differentiate", "contrast")):
            return "Analyze"
        if any(word in lower for word in ("evaluate", "justify", "judge")):
            return "Evaluate"
        if any(word in lower for word in ("design", "create", "compose", "invent")):
            return "Create"
        if any(word in lower for word in ("solve", "calculate", "apply", "use")):
            return "Apply"
        if any(word in lower for word in ("explain", "describe", "why", "how")):
            return "Understand"
        if question_type in {"MCQ", "True / False", "Fill in the Blank"}:
            return "Remember"
        return "Understand"

    def _infer_difficulty(self, text: str, bloom: str) -> str:
        if bloom in {"Analyze", "Evaluate", "Create"}:
            return "Hard"
        if bloom == "Apply":
            return "Medium"
        return "Easy" if len(text) < 80 else "Medium"

    def _heuristic_outcome(self, text: str, outcomes: list[str]) -> list[str]:
        if not outcomes:
            return []
        lower = text.lower()
        best = max(
            outcomes,
            key=lambda outcome: sum(1 for word in outcome.lower().split() if word in lower),
        )
        return [best]
