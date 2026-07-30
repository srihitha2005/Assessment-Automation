"""Runtime configuration.

Everything is env-driven; secrets never live in source. SQLite is the default so a
fresh clone starts with no external dependencies — set DATABASE_URL to a real
Postgres URL for parity with production.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_ROOT.parent


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    api_prefix: str = os.getenv("API_PREFIX", "/api")
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "*")

    database_url: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{(BACKEND_ROOT / 'backend.db').as_posix()}",
    )

    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    ollama_timeout_seconds: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "90"))
    ollama_classify_batch_size: int = int(os.getenv("OLLAMA_CLASSIFY_BATCH_SIZE", "8"))

    question_bank_root: Path = Path(
        os.getenv("QUESTION_BANK_ROOT", str(PROJECT_ROOT / "Question Bank"))
    )
    generated_document_root: Path = Path(
        os.getenv("GENERATED_DOCUMENT_ROOT", str(BACKEND_ROOT / "generated_documents"))
    )
    uploaded_image_root: Path = Path(
        os.getenv("UPLOADED_IMAGE_ROOT", str(BACKEND_ROOT / "uploaded_images"))
    )

    google_spreadsheet_id: str | None = os.getenv("GOOGLE_SPREADSHEET_ID")
    google_service_account_file: str | None = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

    portal_publish_url: str | None = os.getenv("PORTAL_PUBLISH_URL")
    portal_api_key: str | None = os.getenv("PORTAL_API_KEY")
    portal_timeout_seconds: int = int(os.getenv("PORTAL_TIMEOUT_SECONDS", "30"))
    portal_max_retries: int = int(os.getenv("PORTAL_MAX_RETRIES", "3"))

    enable_pdf_export: bool = _bool("ENABLE_PDF_EXPORT", True)
    bootstrap_demo_data: bool = _bool("BOOTSTRAP_DEMO_DATA", True)


settings = Settings()
