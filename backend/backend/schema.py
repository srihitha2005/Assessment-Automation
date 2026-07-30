"""Pydantic request/response models used by every controller.

Uses `alias_generator=camel` so the wire format is camelCase while Python
keeps snake_case attributes.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore",
    )


class ApiResponse(CamelModel):
    success: bool = True
    message: str = ""
    data: Any = None


class GenerateAssessmentRequest(CamelModel):
    planner_id: str | None = None
    curriculum_id: str | None = None
    prompt: str | None = None
    generated_by: str = "SYSTEM"


class UpdateAssessmentRequest(CamelModel):
    status: str | None = None
    total_marks: int | None = Field(default=None, ge=1)
    updated_by: str = "SYSTEM"


class QuestionInput(CamelModel):
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    options: list[str] = Field(default_factory=list)
    question_type: str = "Short Answer"
    difficulty: str = "Medium"
    bloom_level: str = Field(default="Understand", alias="bloomsLevel")
    learning_outcomes: list[str] = Field(default_factory=list)
    marks: int = Field(default=1, ge=1, le=20)
    image: str | None = None
    images: list[Any] = Field(default_factory=list)
    updated_by: str = "SYSTEM"


class QuestionPatch(CamelModel):
    question: str | None = None
    answer: str | None = None
    options: list[str] | None = None
    question_type: str | None = None
    difficulty: str | None = None
    bloom_level: str | None = Field(default=None, alias="bloomsLevel")
    learning_outcomes: list[str] | None = None
    marks: int | None = Field(default=None, ge=1, le=20)
    image: str | None = None
    updated_by: str = "SYSTEM"


class RegenerateRequest(CamelModel):
    prompt: str | None = None
    updated_by: str = "SYSTEM"


class RollbackRequest(CamelModel):
    version: int = Field(ge=1)
    updated_by: str = "SYSTEM"


class CurriculumRequest(CamelModel):
    grade_id: int
    course_id: int
    unit_id: int
    chapter_id: int


class PublishRequest(CamelModel):
    updated_by: str = "SYSTEM"


class SubmissionCreate(CamelModel):
    student_id: str
    student_name: str | None = None
    answers: list[dict] = Field(default_factory=list)


class PlannerOutcomesUpdate(CamelModel):
    learning_outcomes: list[str]
    updated_by: str = "SYSTEM"
