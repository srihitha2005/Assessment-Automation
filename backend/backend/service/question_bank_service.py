"""Reads and appends chapter question banks stored as JSON on disk."""
from __future__ import annotations

import json
import logging

from data.question_bank_index import QuestionBankIndex

logger = logging.getLogger(__name__)


class QuestionBankService:
    def load_questions(self, chapter_name: str) -> list[dict]:
        path = QuestionBankIndex.find(chapter_name)
        if not path:
            logger.warning("Question bank file not found for chapter '%s'.", chapter_name)
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            logger.exception("Could not read question bank file %s.", path)
            return []
        questions = data.get("questions", []) or []
        logger.info("Loaded %s question-bank questions from %s.", len(questions), path.name)
        return [dict(question) for question in questions]

    def append_questions(self, chapter_name: str, questions: list[dict]) -> None:
        if not questions:
            return
        path = QuestionBankIndex.find(chapter_name)
        if not path:
            logger.warning("Generated questions not saved: no bank file for '%s'.", chapter_name)
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            logger.exception("Could not open question bank file %s.", path)
            return
        for question in questions:
            data.setdefault("questions", []).append({
                "question": question.get("question"),
                "answer": question.get("answer"),
                "options": question.get("options", []),
                "image": question.get("image"),
                "images": question.get("images", []),
            })
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        logger.info("Appended %s generated questions to %s.", len(questions), path.name)
