from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from database import Base, GUID


class QuestionImage(Base):
    __tablename__ = "question_image"

    image_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    question_id = Column(
        GUID(),
        ForeignKey("assessment_question.question_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(100))
    size_bytes = Column(Integer)
    uploaded_by = Column(String(100))
    uploaded_on = Column(DateTime, server_default=func.now(), nullable=False)
