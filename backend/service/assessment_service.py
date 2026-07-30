import json
import logging
import math
from collections import Counter
from datetime import datetime
from urllib.request import Request, urlopen

from sqlalchemy.orm import Session

from constants import (
    ASSESSMENT_STATUS_GENERATED,
    ASSESSMENT_STATUS_PARSED,
    ASSESSMENT_STATUS_PUBLISHED,
    BLOOM_MARKS,
    DEFAULT_GENERATED_BY,
    DIFFICULTY_RATIOS,
    MAX_GENERATION_RETRIES,
    QUESTION_TYPES,
)
from config import settings
from data.google_sheets import GoogleSheetsDataSource
from entity.assessment import Assessment
from entity.assessment_question import AssessmentQuestion
from entity.assessment_version import AssessmentVersion
from repository.assessment_question_repository import AssessmentQuestionRepository
from repository.assessment_repository import AssessmentRepository
from repository.assessment_version_repository import AssessmentVersionRepository
from service.document_service import DocumentService
from service.ollama_service import OllamaService
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

    def get_all(self) -> list[dict]:
        return [self._assessment_response(item) for item in self.assessments.get_all()]

    def get_by_id(self, assessment_id) -> dict | None:
        assessment = self.assessments.get_by_id(assessment_id)
        return self._assessment_response(assessment) if assessment else None

    def get_questions(self, assessment_id) -> list[dict]:
        if not self.assessments.get_by_id(assessment_id):
            return []
        return [self._question_response(item) for item in self.questions.get_by_assessment(assessment_id)]

    def get_question(self, question_id) -> dict | None:
        question = self.questions.get_by_id(question_id)
        return self._question_response(question) if question else None

    def generate(self, planner_id: str, generated_by: str = DEFAULT_GENERATED_BY) -> dict:
        context = self.sheets.get_planner_context(planner_id)
        if not context:
            raise ValueError(f"Planner '{planner_id}' was not found in Google Sheets or the sample data.")
        blueprint = self._build_blueprint(context)
        used_questions = self._used_questions(planner_id)
        raw_questions = self.question_bank.load_questions(context["chapterName"])
        available = [item for item in raw_questions if item.get("question", "").strip().lower() not in used_questions]
        logger.info("Generating assessment for planner %s with %s unused bank questions.", planner_id, len(available))

        classified = self.ollama.classify_many(available, context["learningOutcomes"], context["grade"])
        selected, missing = self._select_questions(classified, blueprint)
        if missing:
            logger.info("Generating %s missing questions with %s.", len(missing), settings.ollama_model)
            generated = self._generate_missing(missing, context)
            self.question_bank.append_questions(context["chapterName"], generated)
            selected.extend(generated)

        selected = selected[: blueprint["questionCount"]]
        self._apply_marks(selected, blueprint["totalMarks"])
        self._validate(selected, blueprint, context["learningOutcomes"])

        assessment = Assessment(
            planner_id=planner_id,
            assessment_number=self.assessments.get_next_assessment_number(planner_id),
            version=1,
            total_marks=blueprint["totalMarks"],
            status=ASSESSMENT_STATUS_GENERATED,
            curriculum_id=context.get("curriculumId"),
            grade=context.get("grade"),
            course_name=context.get("courseName"),
            unit_name=context.get("unitName"),
            chapter_name=context.get("chapterName"),
            learning_outcomes=context["learningOutcomes"],
            generated_by=generated_by,
            updated_by=generated_by,
        )
        self.assessments.save(assessment)
        self._replace_questions(assessment, selected, generated_by)
        logger.info("Assessment %s generated successfully.", assessment.assessment_id)
        return self._assessment_response(assessment)

    def regenerate_assessment(self, assessment_id, updated_by: str = DEFAULT_GENERATED_BY) -> dict:
        assessment = self._require_assessment(assessment_id)
        self._save_snapshot(assessment, "REGENERATED", updated_by)
        context = self.sheets.get_planner_context(assessment.planner_id)
        if not context:
            raise ValueError(f"Planner '{assessment.planner_id}' is no longer available.")
        blueprint = self._build_blueprint(context)
        used_questions = self._used_questions(assessment.planner_id) | {item.question.lower().strip() for item in assessment.questions}
        available = [item for item in self.question_bank.load_questions(context["chapterName"]) if item.get("question", "").lower().strip() not in used_questions]
        selected, missing = self._select_questions(self.ollama.classify_many(available, context["learningOutcomes"], context["grade"]), blueprint)
        if missing:
            generated = self._generate_missing(missing, context)
            self.question_bank.append_questions(context["chapterName"], generated)
            selected.extend(generated)
        self._apply_marks(selected, blueprint["totalMarks"])
        self._validate(selected, blueprint, context["learningOutcomes"])
        self.questions.delete_by_assessment(assessment.assessment_id)
        assessment.version += 1
        assessment.total_marks = blueprint["totalMarks"]
        assessment.status = ASSESSMENT_STATUS_GENERATED
        assessment.updated_by = updated_by
        self.assessments.save(assessment)
        self._replace_questions(assessment, selected, updated_by)
        return self._assessment_response(assessment)

    def update_assessment(self, assessment_id, values: dict) -> dict:
        assessment = self._require_assessment(assessment_id)
        self._save_snapshot(assessment, "UPDATED", values.get("updated_by", DEFAULT_GENERATED_BY))
        if values.get("status") is not None:
            assessment.status = values["status"]
        if values.get("total_marks") is not None:
            assessment.total_marks = values["total_marks"]
        assessment.version += 1
        assessment.updated_by = values.get("updated_by", DEFAULT_GENERATED_BY)
        self.assessments.save(assessment)
        return self._assessment_response(assessment)

    def delete_assessment(self, assessment_id) -> None:
        assessment = self._require_assessment(assessment_id)
        self._save_snapshot(assessment, "DELETED", assessment.updated_by or DEFAULT_GENERATED_BY)
        self.assessments.delete(assessment_id)
        logger.info("Deleted assessment %s.", assessment_id)

    def add_question(self, assessment_id, data: dict) -> dict:
        assessment = self._require_assessment(assessment_id)
        self._save_snapshot(assessment, "QUESTION_ADDED", data.get("updated_by", DEFAULT_GENERATED_BY))
        question = AssessmentQuestion(
            assessment_id=assessment.assessment_id,
            question_number=len(assessment.questions) + 1,
            version=assessment.version + 1,
            question=data["question"], answer=data["answer"], options=data.get("options", []),
            question_type=data["question_type"], difficulty=data["difficulty"], bloom_level=data["bloom_level"],
            learning_outcome="; ".join(data.get("learning_outcomes", [])), learning_outcomes=data.get("learning_outcomes", []),
            marks=data["marks"], image=data.get("image"), images=data.get("images", []),
            generated_by=data.get("updated_by", DEFAULT_GENERATED_BY), updated_by=data.get("updated_by", DEFAULT_GENERATED_BY),
        )
        assessment.version += 1
        assessment.total_marks += question.marks
        assessment.updated_by = data.get("updated_by", DEFAULT_GENERATED_BY)
        self.assessments.save(assessment)
        return self._question_response(self.questions.save(question))

    def update_question(self, question_id, data: dict) -> dict:
        question = self._require_question(question_id)
        assessment = self._require_assessment(question.assessment_id)
        self._save_snapshot(assessment, "QUESTION_UPDATED", data.get("updated_by", DEFAULT_GENERATED_BY))
        old_marks = question.marks
        for source, destination in (("question", "question"), ("answer", "answer"), ("options", "options"), ("question_type", "question_type"), ("difficulty", "difficulty"), ("bloom_level", "bloom_level"), ("marks", "marks"), ("image", "image"), ("images", "images")):
            if source in data:
                setattr(question, destination, data[source])
        if "learning_outcomes" in data:
            question.learning_outcomes = data["learning_outcomes"]
            question.learning_outcome = "; ".join(data["learning_outcomes"])
        assessment.version += 1
        question.version = assessment.version
        assessment.total_marks += question.marks - old_marks
        assessment.updated_by = data.get("updated_by", DEFAULT_GENERATED_BY)
        question.updated_by = assessment.updated_by
        self.assessments.save(assessment)
        return self._question_response(self.questions.save(question))

    def delete_question(self, question_id, updated_by: str = DEFAULT_GENERATED_BY) -> None:
        question = self._require_question(question_id)
        assessment = self._require_assessment(question.assessment_id)
        self._save_snapshot(assessment, "QUESTION_DELETED", updated_by)
        assessment.total_marks -= question.marks
        assessment.version += 1
        assessment.updated_by = updated_by
        self.assessments.save(assessment)
        self.questions.delete(question)

    def regenerate_question(self, question_id, prompt: str | None, updated_by: str = DEFAULT_GENERATED_BY) -> dict:
        question = self._require_question(question_id)
        assessment = self._require_assessment(question.assessment_id)
        self._save_snapshot(assessment, "QUESTION_REGENERATED", updated_by)
        requirement = {"learningOutcome": (question.learning_outcomes or assessment.learning_outcomes)[0], "difficulty": question.difficulty, "bloomLevel": question.bloom_level, "questionType": question.question_type, "marks": question.marks}
        generated = self.ollama.generate(requirement, self._assessment_response(assessment), prompt)
        if not generated:
            raise RuntimeError("Qwen could not generate a valid replacement question. Check that Ollama is running.")
        question.question, question.answer = generated["question"], generated["answer"]
        question.options, question.image, question.images = generated.get("options", []), generated.get("image"), generated.get("images", [])
        assessment.version += 1
        question.version, question.updated_by, assessment.updated_by = assessment.version, updated_by, updated_by
        self.assessments.save(assessment)
        return self._question_response(self.questions.save(question))

    def regenerate_answer(self, question_id, updated_by: str = DEFAULT_GENERATED_BY) -> dict:
        question = self._require_question(question_id)
        assessment = self._require_assessment(question.assessment_id)
        self._save_snapshot(assessment, "ANSWER_REGENERATED", updated_by)
        prompt = f'''Give a concise, grade-appropriate model answer for this {assessment.grade} question. Return JSON only as {{"answer":"..."}}.
Question: {question.question}
Learning outcomes: {question.learning_outcomes}'''
        result = self.ollama._generate_json(prompt)
        if not result or not result.get("answer"):
            raise RuntimeError("Qwen could not generate a valid answer. Check that Ollama is running.")
        question.answer = result["answer"]
        assessment.version += 1
        question.version, question.updated_by, assessment.updated_by = assessment.version, updated_by, updated_by
        self.assessments.save(assessment)
        return self._question_response(self.questions.save(question))

    def list_versions(self, assessment_id) -> list[dict]:
        self._require_assessment(assessment_id)
        return [{"version": item.version, "action": item.action, "createdBy": item.created_by, "createdOn": self._date(item.created_on)} for item in self.versions.get_all(assessment_id)]

    def rollback(self, assessment_id, version_number: int, updated_by: str) -> dict:
        assessment = self._require_assessment(assessment_id)
        snapshot = self.versions.get(assessment_id, version_number)
        if not snapshot:
            raise ValueError(f"Version {version_number} was not found.")
        self._save_snapshot(assessment, "ROLLED_BACK", updated_by)
        self.questions.delete_by_assessment(assessment_id)
        data = snapshot.snapshot
        for field, key in (("total_marks", "marks"), ("status", "status"), ("grade", "grade"), ("course_name", "courseName"), ("unit_name", "unitName"), ("chapter_name", "chapterName"), ("learning_outcomes", "learningOutcomes")):
            setattr(assessment, field, data.get(key, getattr(assessment, field)))
        assessment.version += 1
        assessment.updated_by = updated_by
        self.assessments.save(assessment)
        self._replace_questions(assessment, data["questions"], updated_by)
        return self._assessment_response(assessment)

    def create_document(self, assessment_id):
        assessment = self._require_assessment(assessment_id)
        return self.documents.create_docx(self._assessment_response(assessment), self.get_questions(assessment_id))

    def parse_document(self, assessment_id) -> list[dict]:
        path = self.create_document(assessment_id)
        parsed = self.documents.parse_docx(path)
        assessment = self._require_assessment(assessment_id)
        assessment.status = ASSESSMENT_STATUS_PARSED
        self.assessments.save(assessment)
        return parsed

    def publish(self, assessment_id, updated_by: str) -> dict:
        assessment = self._require_assessment(assessment_id)
        payload = self._assessment_response(assessment)
        payload["questions"] = self.get_questions(assessment_id)
        if settings.portal_publish_url:
            request = Request(settings.portal_publish_url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
            try:
                with urlopen(request, timeout=30) as response:
                    if response.status >= 300:
                        raise RuntimeError(f"Portal returned HTTP {response.status}.")
            except Exception as error:
                logger.exception("Portal publishing failed for assessment %s.", assessment_id)
                raise RuntimeError("Portal publishing failed; assessment was not marked as published.") from error
        assessment.status = ASSESSMENT_STATUS_PUBLISHED
        assessment.updated_by = updated_by
        self.assessments.save(assessment)
        return self._assessment_response(assessment)

    def _build_blueprint(self, context: dict) -> dict:
        grade_number = int("".join(character for character in context["grade"] if character.isdigit()) or 6)
        band = "1-2" if grade_number <= 2 else "3-5" if grade_number <= 5 else "6-8" if grade_number <= 8 else "9-10"
        question_count = min(25, max(10, len(context["learningOutcomes"]) * 2))
        difficulty = self._distribute(DIFFICULTY_RATIOS[band], question_count)
        blooms = self._bloom_distribution(band, question_count)
        types = self._distribute({"MCQ": .30, "Short Answer": .25, "True / False": .15, "Fill in the Blank": .15, "Long Answer": .15}, question_count)
        base_marks = sum(BLOOM_MARKS[bloom] for bloom in blooms)
        return {"questionCount": question_count, "difficulty": difficulty, "blooms": blooms, "types": types, "totalMarks": max(10, math.ceil(base_marks / 10) * 10), "outcomes": context["learningOutcomes"]}

    def _bloom_distribution(self, band: str, count: int) -> list[str]:
        ratios = {
            "1-2": {"Remember": .40, "Understand": .40, "Apply": .20},
            "3-5": {"Remember": .25, "Understand": .40, "Apply": .25, "Analyze": .10},
            "6-8": {"Remember": .15, "Understand": .30, "Apply": .30, "Analyze": .20, "Evaluate": .05},
            "9-10": {"Remember": .10, "Understand": .25, "Apply": .30, "Analyze": .20, "Evaluate": .10, "Create": .05},
        }[band]
        return self._distribute(ratios, count)

    @staticmethod
    def _distribute(ratios: dict[str, float], count: int) -> list[str]:
        values = [key for key, ratio in ratios.items() for _ in range(int(count * ratio))]
        remaining = sorted(ratios, key=ratios.get, reverse=True)
        while len(values) < count:
            values.append(remaining[(len(values) - sum(int(count * ratio) for ratio in ratios.values())) % len(remaining)])
        return values[:count]

    def _select_questions(self, candidates: list[dict], blueprint: dict) -> tuple[list[dict], list[dict]]:
        remaining = list(candidates)
        selected, missing = [], []
        for index in range(blueprint["questionCount"]):
            requirement = {"learningOutcome": blueprint["outcomes"][index % len(blueprint["outcomes"])], "difficulty": blueprint["difficulty"][index], "bloomLevel": blueprint["blooms"][index], "questionType": blueprint["types"][index], "marks": BLOOM_MARKS[blueprint["blooms"][index]]}
            if remaining:
                def score(candidate):
                    return (6 if requirement["learningOutcome"] in candidate.get("learningOutcomes", []) else 0) + (5 if candidate.get("difficulty") == requirement["difficulty"] else 0) + (4 if candidate.get("bloomLevel") == requirement["bloomLevel"] else 0) + (3 if candidate.get("questionType") == requirement["questionType"] else 0)
                best = max(remaining, key=score)
                if score(best) >= 6:
                    selected.append(best)
                    remaining.remove(best)
                    continue
            missing.append(requirement)
        return selected, missing

    def _generate_missing(self, missing: list[dict], context: dict) -> list[dict]:
        generated = []
        for requirement in missing:
            item = None
            for _ in range(MAX_GENERATION_RETRIES):
                item = self.ollama.generate(requirement, context)
                if item:
                    generated.append(item)
                    break
            if not item:
                raise RuntimeError("Qwen could not generate all missing questions. Check that Ollama is running and retry.")
        return generated

    @staticmethod
    def _apply_marks(questions: list[dict], total_marks: int) -> None:
        for question in questions:
            question["marks"] = max(1, int(question.get("marks", BLOOM_MARKS.get(question.get("bloomLevel"), 1))))
        difference = total_marks - sum(question["marks"] for question in questions)
        position = 0
        while difference > 0:
            questions[position % len(questions)]["marks"] += 1
            difference -= 1
            position += 1

    @staticmethod
    def _validate(questions: list[dict], blueprint: dict, outcomes: list[str]) -> None:
        if len(questions) != blueprint["questionCount"]:
            raise ValueError("Assessment generation did not produce the required number of questions.")
        if sum(question["marks"] for question in questions) != blueprint["totalMarks"]:
            raise ValueError("Assessment marks do not match the planned total.")
        texts = [question.get("question", "").strip().lower() for question in questions]
        if len(texts) != len(set(texts)):
            raise ValueError("Generated assessment contains duplicate questions.")
        covered = {outcome for question in questions for outcome in question.get("learningOutcomes", [])}
        if not set(outcomes).issubset(covered):
            raise ValueError("Generated assessment does not cover every learning outcome.")

    def _replace_questions(self, assessment: Assessment, questions: list[dict], user: str) -> None:
        entities = [AssessmentQuestion(assessment_id=assessment.assessment_id, question_number=index, version=assessment.version, question=item["question"], answer=item["answer"], options=item.get("options", []), question_type=item.get("questionType", "Short Answer"), difficulty=item.get("difficulty", "Medium"), bloom_level=item.get("bloomLevel", "Understand"), learning_outcome="; ".join(item.get("learningOutcomes", [])), learning_outcomes=item.get("learningOutcomes", []), marks=item["marks"], image=item.get("image"), images=item.get("images", []), generated_by=user, updated_by=user) for index, item in enumerate(questions, start=1)]
        self.questions.save_all(entities)

    def _used_questions(self, planner_id: str) -> set[str]:
        active = self.db.query(AssessmentQuestion.question).join(Assessment).filter(Assessment.planner_id == planner_id).all()
        return {item[0].strip().lower() for item in active} | self.versions.get_question_texts_for_planner(planner_id)

    def _save_snapshot(self, assessment: Assessment, action: str, user: str) -> None:
        self.versions.save(AssessmentVersion(assessment_id=assessment.assessment_id, version=assessment.version, action=action, snapshot=self._assessment_response(assessment, include_questions=True), created_by=user))

    def _assessment_response(self, assessment: Assessment, include_questions: bool = False) -> dict:
        questions = self.questions.get_by_assessment(assessment.assessment_id) if include_questions else list(assessment.questions or [])
        result = {"assessmentId": str(assessment.assessment_id), "plannerId": assessment.planner_id, "assessmentNumber": assessment.assessment_number, "version": assessment.version, "marks": assessment.total_marks, "totalMarks": assessment.total_marks, "status": assessment.status, "curriculumId": assessment.curriculum_id, "grade": assessment.grade, "courseName": assessment.course_name, "unitName": assessment.unit_name, "chapterName": assessment.chapter_name, "learningOutcomes": assessment.learning_outcomes or [], "learningOutcomeCount": len(assessment.learning_outcomes or []), "questionCount": len(questions), "generatedBy": assessment.generated_by, "generatedOn": self._date(assessment.generated_on), "updatedBy": assessment.updated_by, "updatedOn": self._date(assessment.updated_on)}
        if include_questions:
            result["questions"] = [self._question_response(item) for item in questions]
        return result

    def _question_response(self, question: AssessmentQuestion) -> dict:
        return {"questionId": str(question.question_id), "assessmentId": str(question.assessment_id), "questionNumber": question.question_number, "version": question.version, "question": question.question, "answer": question.answer, "options": question.options or [], "questionType": question.question_type, "difficulty": question.difficulty, "bloomsLevel": question.bloom_level, "learningOutcomes": question.learning_outcomes or [], "marks": question.marks, "image": question.image, "images": question.images or [], "generatedBy": question.generated_by, "generatedOn": self._date(question.generated_on), "updatedBy": question.updated_by, "updatedOn": self._date(question.updated_on)}

    @staticmethod
    def _date(value: datetime | None):
        return value.isoformat() if value else None

    def _require_assessment(self, assessment_id) -> Assessment:
        assessment = self.assessments.get_by_id(assessment_id)
        if not assessment:
            raise ValueError("Assessment not found.")
        return assessment

    def _require_question(self, question_id) -> AssessmentQuestion:
        question = self.questions.get_by_id(question_id)
        if not question:
            raise ValueError("Question not found.")
        return question
