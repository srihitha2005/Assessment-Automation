import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class used by all database entities."""


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Provide one database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create tables for a fresh installation. Production changes should use migrations."""
    import entity.assessment  # noqa: F401 - registers entity metadata
    import entity.assessment_question  # noqa: F401
    import entity.assessment_version  # noqa: F401

    logger.info("Creating database tables when they do not exist.")
    Base.metadata.create_all(bind=engine)
