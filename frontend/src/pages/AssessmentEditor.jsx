import "./styles/AssessmentEditor.css";
import "./styles/CurriculumPages.css";

import { useLocation, useNavigate, useParams } from "react-router-dom";
import { CircularProgress } from "@mui/material";

import AssessmentHeader from "../components/Assessment_Components/AssessmentHeader.jsx";
import QuestionCard from "../components/Question_Components/QuestionCard.jsx";
import CurriculumBreadcrumb from "../components/Curriculum_Components/CurriculumBreadcrumb.jsx";
import Button from "../components/Commons/Button.jsx";

import useAssessmentByID from "../hooks/Assessment_Hooks/useAssessmentByID.js";
import useGetAllQuestions from "../hooks/Question_Hooks/useGetAllQuestions.js";

const AssessmentEditor = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { assessmentId, assessmentID } = useParams();
    const id = assessmentId || assessmentID;

    console.log("[AssessmentEditor] Assessment ID:", id);

    const {
        assessment,
        loading: loadingAssessment,
        error: errorAssessment,
        refresh: refreshAssessment
    } = useAssessmentByID(id);

    const {
        questions,
        loading: loadingQuestions,
        error: errorQuestions,
        refresh: refreshQuestions
    } = useGetAllQuestions(id);

    const chapterName = location.state?.chapterName || assessment?.chapterName;
    const gradeId = location.state?.gradeId;
    const courseId = location.state?.courseId;
    const unitId = location.state?.unitId;
    const chapterId = location.state?.chapterId;
    const gradeName = location.state?.gradeName;
    const courseName = location.state?.courseName;
    const unitName = location.state?.unitName;

    const handleRefreshAll = async () => {
        console.log("[AssessmentEditor] Refreshing assessment and questions...");
        await Promise.all([
            refreshAssessment(id),
            refreshQuestions(id)
        ]);
    };

    const handleBack = () => {
        console.log("[AssessmentEditor] Back to assessments clicked.");

        if (gradeId && courseId && unitId && chapterId) {
            navigate(
                `/grades/${gradeId}/courses/${courseId}/units/${unitId}/chapters/${chapterId}/assessments`,
                {
                    state: {
                        gradeName,
                        courseName,
                        unitName,
                        chapterName
                    }
                }
            );
            return;
        }

        navigate("/");
    };

    if (loadingAssessment) {
        return (
            <div className="assessment-editor-message">
                <CircularProgress size={28} sx={{ mr: 1.5 }} />
                Loading Assessment...
            </div>
        );
    }

    if (errorAssessment) {
        return (
            <div className="assessment-editor-message error">
                {errorAssessment}
            </div>
        );
    }

    const breadcrumbItems = [
        { label: "Curriculum", to: "/" }
    ];

    if (gradeId) {
        breadcrumbItems.push({
            label: gradeName || `Grade ${gradeId}`,
            to: `/grades/${gradeId}/courses`
        });
    }

    if (courseId) {
        breadcrumbItems.push({
            label: courseName || `Course ${courseId}`,
            to: `/grades/${gradeId}/courses/${courseId}/units`
        });
    }

    if (unitId) {
        breadcrumbItems.push({
            label: unitName || `Unit ${unitId}`,
            to: `/grades/${gradeId}/courses/${courseId}/units/${unitId}/chapters`
        });
    }

    if (chapterId) {
        breadcrumbItems.push({
            label: chapterName || `Chapter ${chapterId}`,
            to: `/grades/${gradeId}/courses/${courseId}/units/${unitId}/chapters/${chapterId}/assessments`
        });
    }

    breadcrumbItems.push({
        label: `Assessment ${assessment?.assessmentNumber ?? id}`
    });

    return (
        <div className="assessment-editor">
            <CurriculumBreadcrumb items={breadcrumbItems} />

            <div className="page-actions" style={{ justifyContent: "flex-start" }}>
                <Button text="← Back to Assessments" onClick={handleBack} />
            </div>

            <AssessmentHeader
                assessment={assessment}
                chapterName={chapterName}
                onRefresh={handleRefreshAll}
                onDeleted={handleBack}
            />

            {
                loadingQuestions ?
                    (
                        <div className="assessment-editor-message">
                            <CircularProgress size={28} sx={{ mr: 1.5 }} />
                            Loading Questions...
                        </div>
                    )
                    :
                    errorQuestions ?
                        (
                            <div className="assessment-editor-message error">
                                {errorQuestions}
                            </div>
                        )
                        :
                        questions.length === 0 ?
                            (
                                <div className="assessment-editor-message">
                                    No questions found for this assessment.
                                </div>
                            )
                            :
                            (
                                <div className="question-grid">
                                    {
                                        questions.map((question) => (
                                            <QuestionCard
                                                key={question.questionId}
                                                question={question}
                                                learningOutcomes={
                                                    question.learningOutcome
                                                        ? [question.learningOutcome]
                                                        : []
                                                }
                                                onRefresh={handleRefreshAll}
                                            />
                                        ))
                                    }
                                </div>
                            )
            }
        </div>
    );
};

export default AssessmentEditor;
