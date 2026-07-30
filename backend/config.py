import os
from dataclasses import dataclass
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_ROOT.parent


@dataclass(frozen=True)
class Settings:
    """Runtime configuration. Keep secrets in environment variables, never in source code."""

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/assessment_automation",
    )
    ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    question_bank_root: Path = Path(
        os.getenv("QUESTION_BANK_ROOT", str(PROJECT_ROOT / "Question Bank"))
    )
    generated_document_root: Path = Path(
        os.getenv("GENERATED_DOCUMENT_ROOT", str(BACKEND_ROOT / "generated_documents"))
    )
    google_spreadsheet_id: str | None = os.getenv("GOOGLE_SPREADSHEET_ID")
    google_service_account_file: str | None = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    portal_publish_url: str | None = os.getenv("PORTAL_PUBLISH_URL")


settings = Settings()
