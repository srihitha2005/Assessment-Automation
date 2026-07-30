"""End-to-end assessment lifecycle.

Every mutation captures an ``AssessmentVersion`` snapshot inside the same
transaction so rollback is trivially correct. Snapshots use camelCase keys
(the same shape the API returns) and rollback rebuilds questions from that
shape — the historical ``bloomsLevel`` vs ``bloomLevel`` mismatch bug is
fixed by routing every question dict through ``_row_from_dict``.
"""
from __future__ import annotations

import logging
import math
from datetime import datetime
from pathlib import Path
from typing import Iterable

from sqlalchemy.orm import Session

from constants import (
    ACTION_ANSWER_REGENERATED,
    ACTION_DELETED,
    ACTION_GENERATED,
    ACTION_PARSED,
    ACTION_PUBLISHED,
    ACTION_QUESTION_ADDED,
    ACTION_QUESTION_DELETED,
    ACTION_QUESTION_REGENERATED,
    ACTION_QUESTION_UPDATED,
    ACTION_REGENERATED,
    ACTION_ROLLED_BACK,
    ASSESSMENT_STATUS_GENERATED,
    ASSESSMENT_STATUS_PARSED,
    ASSESSMENT_STATUS_PUBLISHED,
    BLOOM_MARKS,
    DEFAULT_USER,
    DIFFICULTY_RATIOS,
    MAX_GENERATION_RETRIES,
    QUESTION_TYPE_RATIOS,
    QUESTION_TYPES,
)
from data.google_sheets import GoogleSheetsDataSource
from entity.assessment import Assessment
from entity.assessment_question import AssessmentQuestion
from entity.assessment_version import AssessmentVersion
from repository.assessment_question_repository import AssessmentQuestionRepository
from repository.assessment_repository import AssessmentRepository
from repository.assessment_version_repository import AssessmentVersionRepository
from service.document_service import DocumentService
from service.ollama_service import OllamaService
from service.publish_service import PublishError, PublishService
from service.question_bank_service import QuestionBankService

logger = logging.getLogger(__name__)


class AssessmentService:
    def __init__(self, db: Session):
        self.db = db
        self.assessments = AssessmentRepository(db)
        self.questions = AssessmentQuestionRepository(db)
        self.versions = AssessmentVersionRepository(db)
        self.sheets = GoogleSheetsDataSource()
        self.question_bank = QuestionBankService()
        self.ollama = OllamaService()
        self.documents = DocumentService()
        self.publisher = PublishService()

    # =========================================================== queries

    def get_all(self) -> list[dict]:
        return [self._assessment_response(item) for item in self.assessments.get_all()]

    def get_by_id(self, assessment_id) -> dict | None:
        assessment = self.assessments.get_by_id(assessment_id)
        return self._assessment_response(assessment) if assessment else None

    def get_questions(self, assessment_id) -> list[dict]:
        if not self.assessments.get_by_id(assessment_id):
            raise LookupError("Assessment not found.")
        return [
            self._question_response(row)
            for row in self.questions.get_by_assessment(assessment_id)
        ]

    def get_question(self, question_id) -> dict:
        question = self._require_question(question_id)
        return self._question_response(question)

    def list_versions(self, assessment_id) -> list[dict]:
        self._require_assessment(assessment_id)
        return [
            {
                "version": item.version,
                "action": item.action,
                "createdBy": item.created_by,
                "createdOn": item.created_on.isoformat() if item.created_on else None,
            }
            for item in self.versions.get_all(assessment_id)
        ]

    # ========================================================== generate

    def generate(
        self,
        planner_id: str | None = None,
        curriculum_id: str | None = None,
        teacher_prompt: str | None = None,
        generated_by: str = DEFAULT_USER,
    ) -> dict:
        planner_id = planner_id or self._planner_from_curriculum(curriculum_id)
        context = self.sheets.get_planner_context(planner_id) if planner_id else None
        if not context:
            raise LookupError("Planner not found for the supplied planner/curriculum id.")

        blueprint = self._build_blueprint(context)
        used = self._used_question_texts(planner_id)
        pool = [
            item
            for item in self.question_bank.load_questions(context["chapterName"])
            if (item.get("question") or "").strip().lower() not in used
        ]
        logger.info(
            "Generating assessment for planner %s (chapter=%s) — %d unused bank questions.",
            planner_id, context["chapterName"], len(pool),
        )

        classified = self.ollama.classify_many(pool, context["learningOutcomes"], context["grade"])
        selected, gaps = self._select(classified, blueprint)
        if gaps:
            logger.info("Filling %d gaps via LLM generation.", len(gaps))
            fresh = self._generate_missing(gaps, context, teacher_prompt)
            if fresh:
                self.question_bank.append_questions(context["chapterName"], fresh)
            selected.extend(fresh)

        selected = selected[: blueprint["questionCount"]]
        self._apply_marks(selected, blueprint["totalMarks"])
        report = self._validation_report(selected, blueprint, context["learningOutcomes"])

        assessment = Assessment(
            planner_id=planner_id,
            curriculum_id=context.get("curriculumId"),
            assessment_number=self.assessments.get_next_assessment_number(planner_id),
            version=1,
            total_marks=sum(item["marks"] for item in selected),
            status=ASSESSMENT_STATUS_GENERATED,
            grade=context.get("grade"),
            course_name=context.get("courseName"),
            unit_name=context.get("unitName"),
            chapter_name=context.get("chapterName"),
            learning_outcomes=list(context["learningOutcomes"]),
            validation_report=report,
            generated_by=generated_by,
            updated_by=generated_by,
        )
        self.assessments.save(assessment)
        self._replace_questions(assessment, selected, generated_by)
        self._snapshot(assessment, ACTION_GENERATED, generated_by)
        logger.info("Assessment %s generated (%d questions, %d marks).",
                    assessment.assessment_id, len(selected), assessment.total_marks)
        return self._assessment_response(assessment)

    # =========================================================== update

    def regenerate(self, assessment_id, teacher_prompt: str | None, user: str = DEFAULT_USER) -> dict:
        assessment = self._require_assessment(assessment_id)
        self._snapshot(assessment, ACTION_REGENERATED, user)
        context = self.sheets.get_planner_context(assessment.planner_id)
        if not context:
            raise LookupError("Planner is no longer available.")
        # Refresh the outcomes on the assessment so the new run reflects planner edits.
        assessment.learning_outcomes = list(context["learningOutcomes"])
        blueprint = self._build_blueprint(context)
        already = self._used_question_texts(assessment.planner_id) | {
            (row.question or "").strip().lower() for row in assessment.questions
        }
        pool = [
            item
            for item in self.question_bank.load_questions(context["chapterName"])
            if (item.get("question") or "").strip().lower() not in already
        ]
        classified = self.ollama.classify_many(pool, context["learningOutcomes"], context["grade"])
        selected, gaps = self._select(classified, blueprint)
        if gaps:
            fresh = self._generate_missing(gaps, context, teacher_prompt)
            if fresh:
                self.question_bank.append_questions(context["chapterName"], fresh)
            selected.extend(fresh)
        selected = selected[: blueprint["questionCount"]]
        self._apply_marks(selected, blueprint["totalMarks"])
        report = self._validation_report(selected, blueprint, context["learningOutcomes"])
        self.questions.delete_by_assessment(assessment.assessment_id)
        assessment.version += 1
        assessment.total_marks = sum(item["marks"] for item in selected)
        assessment.status = ASSESSMENT_STATUS_GENERATED
        assessment.validation_report = report
        assessment.updated_by = user
        self.assessments.save(assessment)
        self._replace_questions(assessment, selected, user)
        return self._assessment_response(assessment)

    def delete(self, assessment_id, user: str = DEFAULT_USER) -> None:
        assessment = self._require_assessment(assessment_id)
        self._snapshot(assessment, ACTION_DELETED, user)
        self.assessments.delete(assessment_id)

    # ========================================================= questions

    def update_question(self, question_id, data: dict) -> dict:
        question = self._require_question(question_id)
        assessment = self._require_assessment(question.assessment_id)
        user = data.get("updated_by", DEFAULT_USER)
        self._snapshot(assessment, ACTION_QUESTION_UPDATED, user)
        old_marks = question.marks
        mapping = {
            "question": "question",
            "answer": "answer",
            "options": "options",
            "question_type": "question_type",
            "difficulty": "difficulty",
            "bloom_level": "bloom_level",
            "learning_outcomes": "learning_outcomes",
            "marks": "marks",
            "image": "image",
        }
        for source, target in mapping.items():
            if data.get(source) is not None:
                setattr(question, target, data[source])
        assessment.version += 1
        assessment.total_marks += question.marks - old_marks
        assessment.updated_by = user
        question.version = assessment.version
        question.updated_by = user
        self.assessments.save(assessment)
        return self._question_response(self.questions.save(question))

    def delete_question(self, question_id, user: str = DEFAULT_USER) -> None:
        question = self._require_question(question_id)
        assessment = self._require_assessment(question.assessment_id)
        self._snapshot(assessment, ACTION_QUESTION_DELETED, user)
        assessment.total_marks = max(0, (assessment.total_marks or 0) - (question.marks or 0))
        assessment.version += 1
        assessment.updated_by = user
        self.assessments.save(assessment)
        self.questions.delete(question)

    def regenerate_question(
        self, question_id, teacher_prompt: str | None, user: str = DEFAULT_USER
    ) -> dict:
        question = self._require_question(question_id)
        assessment = self._require_assessment(question.assessment_id)
        self._snapshot(assessment, ACTION_QUESTION_REGENERATED, user)
        outcome = (question.learning_outcomes or assessment.learning_outcomes or [""])[0]
        requirement = {
            "learningOutcome": outcome,
            "difficulty": question.difficulty,
            "bloomLevel": question.bloom_level,
            "questionType": question.question_type,
            "marks": question.marks,
        }
        context = {
            "grade": assessment.grade,
            "chapterName": assessment.chapter_name,
        }
        candidate = None
        for _ in range(MAX_GENERATION_RETRIES):
            candidate = self.ollama.generate(requirement, context, teacher_prompt)
            if candidate:
                break
        if not candidate:
            raise RuntimeError("Local model failed to produce a replacement question. Check Ollama.")
        question.question = candidate["question"]
        question.answer = candidate["answer"]
        question.options = candidate.get("options", []) or []
        question.image = candidate.get("image") or question.image
        assessment.version += 1
        question.version = assessment.version
        question.updated_by = user
        assessment.updated_by = user
        self.assessments.save(assessment)
        return self._question_response(self.questions.save(question))

    def regenerate_answer(self, question_id, teacher_prompt: str | None, user: str = DEFAULT_USER) -> dict:
        question = self._require_question(question_id)
        assessment = self._require_assessment(question.assessment_id)
        self._snapshot(assessment, ACTION_ANSWER_REGENERATED, user)
        answer = self.ollama.regenerate_answer(
            question.question, question.learning_outcomes or [], assessment.grade or "middle school",
            teacher_prompt,
        )
        if not answer:
            raise RuntimeError("Local model failed to produce an answer. Check Ollama.")
        question.answer = answer
        assessment.version += 1
        question.version = assessment.version
        question.updated_by = user
        assessment.updated_by = user
        self.assessments.save(assessment)
        return self._question_response(self.questions.save(question))

    def add_question(self, assessment_id, data: dict) -> dict:
        assessment = self._require_assessment(assessment_id)
        user = data.get("updated_by", DEFAULT_USER)
        self._snapshot(assessment, ACTION_QUESTION_ADDED, user)
        rows = self.questions.get_by_assessment(assessment.assessment_id)
        number = (rows[-1].question_number + 1) if rows else 1
        question = AssessmentQuestion(
            assessment_id=assessment.assessment_id,
            question_number=number,
            version=assessment.version + 1,
            question=data["question"],
            answer=data["answer"],
            options=data.get("options", []),
            question_type=data.get("question_type", "Short Answer"),
            difficulty=data.get("difficulty", "Medium"),
            bloom_level=data.get("bloom_level", "Understand"),
            learning_outcomes=data.get("learning_outcomes") or (assessment.learning_outcomes or [])[:1],
            marks=data.get("marks", 1),
            image=data.get("image"),
            images=data.get("images", []),
            generated_by=user,
            updated_by=user,
        )
        assessment.version += 1
        assessment.total_marks += question.marks
        assessment.updated_by = user
        self.assessments.save(assessment)
        return self._question_response(self.questions.save(question))

    # ========================================================== rollback

    def rollback(self, assessment_id, version_number: int, user: str = DEFAULT_USER) -> dict:
        assessment = self._require_assessment(assessment_id)
        snapshot = self.versions.get(assessment_id, version_number)
        if not snapshot:
            raise LookupError(f"Version {version_number} not found for this assessment.")
        self._snapshot(assessment, ACTION_ROLLED_BACK, user)
        data = snapshot.snapshot
        for target, key in (
            ("total_marks", "totalMarks"),
            ("status", "status"),
            ("grade", "grade"),
            ("course_name", "courseName"),
            ("unit_name", "unitName"),
            ("chapter_name", "chapterName"),
            ("learning_outcomes", "learningOutcomes"),
            ("validation_report", "validationReport"),
        ):
            if key in data and data[key] is not None:
                setattr(assessment, target, data[key])
        assessment.version += 1
        assessment.updated_by = user
        self.assessments.save(assessment)
        self.questions.delete_by_assessment(assessment_id)
        self._replace_questions(assessment, data.get("questions", []), user)
        return self._assessment_response(assessment)

    # =================================================== documents / publish

    def create_docx(self, assessment_id) -> Path:
        assessment = self._require_assessment(assessment_id)
        return self.documents.create_docx(
            self._assessment_response(assessment),
            [self._question_response(row) for row in self.questions.get_by_assessment(assessment_id)],
        )

    def create_pdf(self, assessment_id) -> Path:
        assessment = self._require_assessment(assessment_id)
        return self.documents.create_pdf(
            self._assessment_response(assessment),
            [self._question_response(row) for row in self.questions.get_by_assessment(assessment_id)],
        )

    def parse(self, assessment_id, user: str = DEFAULT_USER) -> dict:
        assessment = self._require_assessment(assessment_id)
        path = self.create_docx(assessment_id)
        parsed = self.documents.parse_docx(path)
        assessment.status = ASSESSMENT_STATUS_PARSED
        assessment.updated_by = user
        self.assessments.save(assessment)
        self._snapshot(assessment, ACTION_PARSED, user)
        return {
            "assessmentId": str(assessment.assessment_id),
            "source": parsed["source"],
            "questions": parsed["questions"],
            "documentPath": path.as_posix(),
        }

    def publish(self, assessment_id, user: str = DEFAULT_USER) -> dict:
        assessment = self._require_assessment(assessment_id)
        payload = self._assessment_response(assessment)
        payload["questions"] = [
            self._question_response(row) for row in self.questions.get_by_assessment(assessment_id)
        ]
        try:
            receipt = self.publisher.publish(payload)
        except PublishError as error:
            raise RuntimeError(str(error)) from error
        assessment.status = ASSESSMENT_STATUS_PUBLISHED
        assessment.publish_target = receipt.get("target")
        assessment.publish_digest = receipt.get("digest")
        assessment.published_on = datetime.utcnow()
        assessment.updated_by = user
        self.assessments.save(assessment)
        self._snapshot(assessment, ACTION_PUBLISHED, user)
        return {"assessment": self._assessment_response(assessment), "receipt": receipt}

    # ================================================================ helpers

    def _planner_from_curriculum(self, curriculum_id: str | None) -> str | None:
        if not curriculum_id:
            return None
        planner = next(
            (item for item in self.sheets.get_planners() if item["curriculumId"] == curriculum_id),
            None,
        )
        return planner["plannerId"] if planner else None

    def _build_blueprint(self, context: dict) -> dict:
        grade_digits = "".join(ch for ch in context.get("grade", "") if ch.isdigit()) or "6"
        grade = int(grade_digits)
        band = "1-2" if grade <= 2 else "3-5" if grade <= 5 else "6-8" if grade <= 8 else "9-10"
        question_count = min(20, max(8, len(context.get("learningOutcomes") or []) * 3))
        difficulty = self._distribute(DIFFICULTY_RATIOS[band], question_count)
        blooms = self._distribute(self._bloom_ratios(band), question_count)
        types = self._distribute(QUESTION_TYPE_RATIOS, question_count)
        base_marks = sum(BLOOM_MARKS[bloom] for bloom in blooms)
        total_marks = max(10, math.ceil(base_marks / 5) * 5)
        return {
            "questionCount": question_count,
            "difficulty": difficulty,
            "blooms": blooms,
            "types": types,
            "totalMarks": total_marks,
            "outcomes": list(context.get("learningOutcomes") or []),
        }

    @staticmethod
    def _bloom_ratios(band: str) -> dict[str, float]:
        return {
            "1-2": {"Remember": 0.40, "Understand": 0.40, "Apply": 0.20},
            "3-5": {"Remember": 0.25, "Understand": 0.40, "Apply": 0.25, "Analyze": 0.10},
            "6-8": {"Remember": 0.15, "Understand": 0.30, "Apply": 0.30, "Analyze": 0.20, "Evaluate": 0.05},
            "9-10": {"Remember": 0.10, "Understand": 0.25, "Apply": 0.30, "Analyze": 0.20, "Evaluate": 0.10, "Create": 0.05},
        }[band]

    @staticmethod
    def _distribute(ratios: dict[str, float], count: int) -> list[str]:
        values: list[str] = []
        for key, ratio in ratios.items():
            values.extend([key] * int(count * ratio))
        preferred = sorted(ratios, key=ratios.get, reverse=True)
        while len(values) < count:
            values.append(preferred[len(values) % len(preferred)])
        return values[:count]

    def _select(self, candidates: list[dict], blueprint: dict) -> tuple[list[dict], list[dict]]:
        remaining = list(candidates)
        selected: list[dict] = []
        gaps: list[dict] = []
        outcomes = blueprint["outcomes"] or [""]
        for index in range(blueprint["questionCount"]):
            requirement = {
                "learningOutcome": outcomes[index % len(outcomes)],
                "difficulty": blueprint["difficulty"][index],
                "bloomLevel": blueprint["blooms"][index],
                "questionType": blueprint["types"][index],
                "marks": BLOOM_MARKS[blueprint["blooms"][index]],
            }
            if remaining:
                def score(candidate, req=requirement):
                    return (
                        (6 if req["learningOutcome"] in candidate.get("learningOutcomes", []) else 0)
                        + (5 if candidate.get("difficulty") == req["difficulty"] else 0)
                        + (4 if candidate.get("bloomLevel") == req["bloomLevel"] else 0)
                        + (3 if candidate.get("questionType") == req["questionType"] else 0)
                    )

                best = max(remaining, key=score)
                if score(best) >= 6:
                    selected.append(best)
                    remaining.remove(best)
                    continue
            gaps.append(requirement)
        return selected, gaps

    def _generate_missing(self, gaps: list[dict], context: dict, teacher_prompt: str | None) -> list[dict]:
        generated: list[dict] = []
        for requirement in gaps:
            candidate = None
            for _ in range(MAX_GENERATION_RETRIES):
                candidate = self.ollama.generate(requirement, context, teacher_prompt)
                if candidate:
                    break
            if candidate:
                generated.append(candidate)
            else:
                # Deterministic placeholder rather than raising — flagged for teacher review.
                generated.append(
                    {
                        "question": self._placeholder_question(requirement, context),
                        "answer": "[needs teacher review]",
                        "options": [],
                        "difficulty": requirement["difficulty"],
                        "bloomLevel": requirement["bloomLevel"],
                        "questionType": requirement["questionType"],
                        "marks": requirement["marks"],
                        "learningOutcomes": [requirement["learningOutcome"]],
                        "needsReview": True,
                    }
                )
        return generated

    @staticmethod
    def _placeholder_question(requirement: dict, context: dict) -> str:
        return (
            f"[Placeholder — {requirement['difficulty']} {requirement['bloomLevel']} "
            f"{requirement['questionType']}] Write a question on \"{requirement['learningOutcome']}\" "
            f"for {context.get('grade', 'this grade')}, chapter \"{context.get('chapterName')}\"."
        )

    @staticmethod
    def _apply_marks(questions: list[dict], total_marks: int) -> None:
        for question in questions:
            marks = question.get("marks") or BLOOM_MARKS.get(question.get("bloomLevel"), 1)
            question["marks"] = max(1, int(marks))
        diff = total_marks - sum(question["marks"] for question in questions)
        i = 0
        while diff > 0 and questions:
            questions[i % len(questions)]["marks"] += 1
            diff -= 1
            i += 1
        while diff < 0 and questions:
            if questions[i % len(questions)]["marks"] > 1:
                questions[i % len(questions)]["marks"] -= 1
                diff += 1
            i += 1

    @staticmethod
    def _validation_report(questions: list[dict], blueprint: dict, outcomes: list[str]) -> dict:
        texts = [(question.get("question") or "").strip().lower() for question in questions]
        duplicates = [text for text in set(texts) if texts.count(text) > 1 and text]
        covered = {outcome for question in questions for outcome in question.get("learningOutcomes", [])}
        missing_outcomes = [outcome for outcome in outcomes if outcome not in covered]
        return {
            "questionCount": len(questions),
            "expectedCount": blueprint["questionCount"],
            "totalMarks": sum(question.get("marks", 0) for question in questions),
            "expectedMarks": blueprint["totalMarks"],
            "duplicateQuestions": duplicates,
            "missingOutcomes": missing_outcomes,
            "needsReview": any(question.get("needsReview") for question in questions),
        }

    def _replace_questions(
        self, assessment: Assessment, items: Iterable[dict], user: str
    ) -> None:
        rows = [
            self._row_from_dict(assessment, item, index, user)
            for index, item in enumerate(items, start=1)
        ]
        if rows:
            self.questions.save_all(rows)

    @staticmethod
    def _row_from_dict(assessment: Assessment, item: dict, number: int, user: str) -> AssessmentQuestion:
        bloom = item.get("bloomLevel") or item.get("bloomsLevel") or "Understand"
        question_type = item.get("questionType") or item.get("question_type") or "Short Answer"
        difficulty = item.get("difficulty") or "Medium"
        outcomes = item.get("learningOutcomes") or item.get("learning_outcomes") or []
        return AssessmentQuestion(
            assessment_id=assessment.assessment_id,
            question_number=item.get("questionNumber") or number,
            version=assessment.version,
            question=item["question"],
            answer=item.get("answer", ""),
            options=item.get("options", []) or [],
            question_type=question_type if question_type in QUESTION_TYPES else "Short Answer",
            difficulty=difficulty,
            bloom_level=bloom,
            learning_outcomes=list(outcomes),
            marks=max(1, int(item.get("marks") or BLOOM_MARKS.get(bloom, 1))),
            image=item.get("image"),
            images=item.get("images", []) or [],
            needs_review=bool(item.get("needsReview") or item.get("needs_review")),
            generated_by=item.get("generatedBy") or user,
            updated_by=user,
        )

    def _used_question_texts(self, planner_id: str) -> set[str]:
        active = (
            self.db.query(AssessmentQuestion.question)
            .join(Assessment, Assessment.assessment_id == AssessmentQuestion.assessment_id)
            .filter(Assessment.planner_id == planner_id)
            .all()
        )
        used = {(row[0] or "").strip().lower() for row in active}
        used |= self.versions.get_question_texts_for_planner(planner_id)
        return used

    def _snapshot(self, assessment: Assessment, action: str, user: str) -> None:
        payload = self._assessment_response(assessment)
        payload["questions"] = [
            self._question_response(row)
            for row in self.questions.get_by_assessment(assessment.assessment_id)
        ]
        self.versions.save(
            AssessmentVersion(
                assessment_id=assessment.assessment_id,
                version=assessment.version,
                action=action,
                snapshot=payload,
                created_by=user,
            )
        )

    # ------------------------------------------------------------- serialize

    def _assessment_response(self, assessment: Assessment) -> dict:
        questions = list(assessment.questions or [])
        return {
            "assessmentId": str(assessment.assessment_id),
            "plannerId": assessment.planner_id,
            "curriculumId": assessment.curriculum_id,
            "assessmentNumber": assessment.assessment_number,
            "version": assessment.version,
            "totalMarks": assessment.total_marks,
            "marks": assessment.total_marks,
            "status": assessment.status,
            "grade": assessment.grade,
            "courseName": assessment.course_name,
            "unitName": assessment.unit_name,
            "chapterName": assessment.chapter_name,
            "learningOutcomes": assessment.learning_outcomes or [],
            "learningOutcomeCount": len(assessment.learning_outcomes or []),
            "questionCount": len(questions),
            "validationReport": assessment.validation_report or {},
            "publishTarget": assessment.publish_target,
            "publishDigest": assessment.publish_digest,
            "publishedOn": assessment.published_on.isoformat() if assessment.published_on else None,
            "generatedBy": assessment.generated_by,
            "generatedOn": assessment.generated_on.isoformat() if assessment.generated_on else None,
            "updatedBy": assessment.updated_by,
            "updatedOn": assessment.updated_on.isoformat() if assessment.updated_on else None,
        }

    def _question_response(self, question: AssessmentQuestion) -> dict:
        return {
            "questionId": str(question.question_id),
            "assessmentId": str(question.assessment_id),
            "questionNumber": question.question_number,
            "version": question.version,
            "question": question.question,
            "answer": question.answer,
            "options": question.options or [],
            "questionType": question.question_type,
            "difficulty": question.difficulty,
            "bloomsLevel": question.bloom_level,
            "bloomLevel": question.bloom_level,
            "learningOutcomes": question.learning_outcomes or [],
            "marks": question.marks,
            "image": question.image,
            "images": question.images or [],
            "needsReview": bool(question.needs_review),
            "generatedBy": question.generated_by,
            "generatedOn": question.generated_on.isoformat() if question.generated_on else None,
            "updatedBy": question.updated_by,
            "updatedOn": question.updated_on.isoformat() if question.updated_on else None,
        }

    def _require_assessment(self, assessment_id) -> Assessment:
        assessment = self.assessments.get_by_id(assessment_id)
        if not assessment:
            raise LookupError("Assessment not found.")
        return assessment

    def _require_question(self, question_id) -> AssessmentQuestion:
        question = self.questions.get_by_id(question_id)
        if not question:
            raise LookupError("Question not found.")
        return question
