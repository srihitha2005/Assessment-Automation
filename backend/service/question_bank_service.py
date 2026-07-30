import json
import logging
import re
from pathlib import Path

from config import settings

logger = logging.getLogger(__name__)


def normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


class QuestionBankService:
    """Reads and appends questions using the simple JSON structure in the repository."""

    def find_chapter_file(self, chapter_name: str) -> Path | None:
        target = normalise(chapter_name)
        for path in settings.question_bank_root.rglob("*.json"):
            if normalise(path.stem) == target:
                return path
        return None

    def load_questions(self, chapter_name: str) -> list[dict]:
        path = self.find_chapter_file(chapter_name)
        if not path:
            logger.warning("Question bank file not found for chapter '%s'.", chapter_name)
            return []
        try:
            with path.open(encoding="utf-8") as file:
                data = json.load(file)
            questions = data.get("questions", [])
            logger.info("Loaded %s question-bank questions from %s.", len(questions), path.name)
            return [dict(question) for question in questions]
        except (OSError, json.JSONDecodeError):
            logger.exception("Could not read question bank file %s.", path)
            return []

    def append_questions(self, chapter_name: str, questions: list[dict]) -> None:
        path = self.find_chapter_file(chapter_name)
        if not path:
            logger.warning("Generated questions were not saved: no question-bank file for '%s'.", chapter_name)
            return
        try:
            with path.open(encoding="utf-8") as file:
                data = json.load(file)
            data.setdefault("questions", []).extend(questions)
            with path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            logger.info("Saved %s generated questions to %s.", len(questions), path.name)
        except (OSError, json.JSONDecodeError):
            logger.exception("Could not append generated questions to %s.", path)
