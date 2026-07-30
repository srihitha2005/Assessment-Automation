from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class GenerateAssessmentRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    planner_id: str = Field(validation_alias="plannerId")
    generated_by: str = Field(default="SYSTEM", validation_alias="generatedBy")


class UpdateAssessmentRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    status: str | None = None
    total_marks: int | None = Field(default=None, ge=1, validation_alias="totalMarks")
    updated_by: str = Field(default="SYSTEM", validation_alias="updatedBy")


class QuestionInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    options: list[str] = Field(default_factory=list)
    question_type: str = Field(default="Short Answer", validation_alias="questionType")
    difficulty: str = "Medium"
    bloom_level: str = Field(default="Understand", validation_alias="bloomsLevel")
    learning_outcomes: list[str] = Field(default_factory=list, validation_alias="learningOutcomes")
    marks: int = Field(default=1, ge=1, le=20)
    image: str | None = None
    images: list[Any] = Field(default_factory=list)
    updated_by: str = Field(default="SYSTEM", validation_alias="updatedBy")


class RegenerateQuestionRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    prompt: str | None = None
    updated_by: str = Field(default="SYSTEM", validation_alias="updatedBy")


class RollbackRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    version: int = Field(ge=1)
    updated_by: str = Field(default="SYSTEM", validation_alias="updatedBy")


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Any = None
