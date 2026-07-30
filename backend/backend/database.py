"""Database engine, session factory, and a dialect-neutral GUID type.

SQLite is the default so `uvicorn main:app` starts with zero external services.
Set DATABASE_URL to a `postgresql+psycopg://...` URL for production parity — the
same schema works on either backend because `GUID` decays to `CHAR(36)` on SQLite
and native `UUID` on PostgreSQL.
"""
from __future__ import annotations

import logging
import uuid

from sqlalchemy import CHAR, create_engine
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.types import TypeDecorator

from config import settings

logger = logging.getLogger(__name__)


class GUID(TypeDecorator):
    """Platform-independent UUID column: native UUID on PostgreSQL, CHAR(36) elsewhere."""

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(str(value))
        if dialect.name == "postgresql":
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))


class Base(DeclarativeBase):
    """Base class for every ORM entity."""


connect_args: dict = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency: one session per request."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Create tables when missing. Use Alembic if you outgrow this."""
    from entity import assessment, assessment_question, assessment_version  # noqa: F401
    from entity import submission, propagation_event  # noqa: F401
    from entity import question_image  # noqa: F401

    logger.info("Ensuring database schema exists on %s", engine.url.render_as_string(hide_password=True))
    Base.metadata.create_all(bind=engine)
