import json
import logging
import re
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from config import settings
from constants import BLOOM_MARKS, QUESTION_TYPES

logger = logging.getLogger(__name__)


class OllamaService:
    """Minimal local Ollama client. Only qwen2.5:3b is used by configuration."""

    def _generate_json(self, prompt: str) -> dict | None:
        request = Request(
            f"{settings.ollama_url.rstrip('/')}/api/generate",
            data=json.dumps({"model": settings.ollama_model, "prompt": prompt, "format": "json", "stream": False}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=90) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return json.loads(payload["response"])
        except (HTTPError, URLError, TimeoutError, KeyError, json.JSONDecodeError):
            logger.warning("Ollama did not return valid JSON; using deterministic fallback.", exc_info=True)
            return None

    def classify(self, question: dict, learning_outcomes: list[str], grade: str) -> dict:
        prompt = f'''Classify this school assessment question for {grade}.
Learning outcomes: {json.dumps(learning_outcomes)}
Question: {json.dumps(question.get("question", ""))}
Allowed question types: {QUESTION_TYPES}
Return JSON only: {{"difficulty":"Easy|Medium|Hard","bloomLevel":"Remember|Understand|Apply|Analyze|Evaluate|Create","questionType":"...","learningOutcomes":["exact supplied outcomes"],"marks":1}}.'''
        result = self._generate_json(prompt)
        return self._validate_classification(result, question, learning_outcomes)

    def classify_many(self, questions: list[dict], learning_outcomes: list[str], grade: str) -> list[dict]:
        """Classify a chapter in one local-model request, rather than one slow call per question."""
        prompt = f'''Classify each question for a {grade} assessment.
Learning outcomes: {json.dumps(learning_outcomes)}
Allowed question types: {QUESTION_TYPES}
Return JSON only as {{"classifications":[{{"index":0,"difficulty":"Easy|Medium|Hard","bloomLevel":"Remember|Understand|Apply|Analyze|Evaluate|Create","questionType":"...","learningOutcomes":["exact supplied outcome"],"marks":1}}]}}.
Questions: {json.dumps([item.get("question", "") for item in questions])}'''
        result = self._generate_json(prompt) or {}
        classified_by_index = {
            item.get("index"): item
            for item in result.get("classifications", [])
            if isinstance(item, dict) and isinstance(item.get("index"), int)
        }
        return [
            self._validate_classification(classified_by_index.get(index), question, learning_outcomes)
            for index, question in enumerate(questions)
        ]

    def generate(self, requirement: dict, context: dict, teacher_prompt: str | None = None) -> dict | None:
        prompt = f'''Create one original {context["grade"]} assessment question. Return JSON only.
Chapter: {context["chapterName"]}
Learning outcome: {requirement["learningOutcome"]}
Required difficulty: {requirement["difficulty"]}; Bloom level: {requirement["bloomLevel"]}; type: {requirement["questionType"]}; marks: {requirement["marks"]}.
Adapt vocabulary and cognitive load to the grade. Do not repeat a known question. For MCQ and True / False include options.
{teacher_prompt or ""}
Schema: {{"question":"...","answer":"...","options":[],"image":null,"images":[]}}'''
        generated = self._generate_json(prompt)
        if not generated or not generated.get("question") or not generated.get("answer"):
            return None
        return {**generated, **requirement, "learningOutcomes": [requirement["learningOutcome"]]}

    def _validate_classification(self, result: dict | None, question: dict, outcomes: list[str]) -> dict:
        text = question.get("question", "")
        options = question.get("options", [])
        if result is None:
            if len(options) == 2 and {item.lower() for item in options} == {"true", "false"}:
                question_type = "True / False"
            elif len(options) >= 3:
                question_type = "MCQ"
            elif "fill in the blank" in text.lower() or "____" in text:
                question_type = "Fill in the Blank"
            elif len(text) > 150 or any(word in text.lower() for word in ("compare", "analyse", "analyze", "explain why")):
                question_type = "Long Answer"
            else:
                question_type = "Short Answer"
            bloom = "Understand" if question_type != "MCQ" else "Remember"
            result = {"difficulty": "Medium", "bloomLevel": bloom, "questionType": question_type, "learningOutcomes": outcomes[:1], "marks": BLOOM_MARKS[bloom]}

        bloom = result.get("bloomLevel", "Understand")
        if bloom not in BLOOM_MARKS:
            bloom = "Understand"
        question_type = result.get("questionType", "Short Answer")
        if question_type not in QUESTION_TYPES:
            question_type = "Short Answer"
        matched_outcomes = [outcome for outcome in result.get("learningOutcomes", []) if outcome in outcomes]
        if not matched_outcomes:
            lower_text = text.lower()
            if any(word in lower_text for word in ("difference", "similar", "both", "compare")):
                matched_outcomes = [next((outcome for outcome in outcomes if any(word in outcome.lower() for word in ("compare", "differentiate"))), outcomes[0])]
            elif any(word in lower_text for word in ("function", "role", "controls", "why")):
                matched_outcomes = [next((outcome for outcome in outcomes if any(word in outcome.lower() for word in ("explain", "describe", "function"))), outcomes[0])]
            else:
                matched_outcomes = outcomes[:1]
        return {
            **question,
            "difficulty": result.get("difficulty") if result.get("difficulty") in {"Easy", "Medium", "Hard"} else "Medium",
            "bloomLevel": bloom,
            "questionType": question_type,
            "learningOutcomes": matched_outcomes,
            "marks": max(1, min(20, int(result.get("marks", BLOOM_MARKS[bloom])))),
        }
