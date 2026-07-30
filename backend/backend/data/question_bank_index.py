"""One-time index over the ``Question Bank`` directory.

Avoids `Path.rglob` on every request. Rebuild via `QuestionBankIndex.refresh()`
if the tree changes at runtime (e.g. tests dropping files in a tmp dir).
"""
from __future__ import annotations

import logging
import re
from pathlib import Path
from threading import Lock

from config import settings

logger = logging.getLogger(__name__)


def normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


class QuestionBankIndex:
    _map: dict[str, Path] = {}
    _lock: Lock = Lock()
    _built: bool = False

    @classmethod
    def _build(cls) -> None:
        root = settings.question_bank_root
        mapping: dict[str, Path] = {}
        if root.exists():
            for path in root.rglob("*.json"):
                mapping[normalise(path.stem)] = path
        else:
            logger.warning("Question bank root not found at %s", root)
        cls._map = mapping
        cls._built = True
        logger.info("Indexed %s chapter files under %s", len(mapping), root)

    @classmethod
    def refresh(cls) -> None:
        with cls._lock:
            cls._build()

    @classmethod
    def _ensure_built(cls) -> None:
        if not cls._built:
            with cls._lock:
                if not cls._built:
                    cls._build()

    @classmethod
    def find(cls, chapter_name: str) -> Path | None:
        cls._ensure_built()
        return cls._map.get(normalise(chapter_name))

    @classmethod
    def all_chapters(cls) -> list[str]:
        cls._ensure_built()
        return sorted(path.stem for path in cls._map.values())
