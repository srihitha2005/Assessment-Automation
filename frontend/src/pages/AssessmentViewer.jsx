import "./styles/AssessmentViewer.css";
import "./styles/CurriculumPages.css";

import { useState } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { CircularProgress } from "@mui/material";

import AssesssmentCard from "../components/Assessment_Components/AssesssmentCard.jsx";
import CurriculumBreadcrumb from "../components/Curriculum_Components/CurriculumBreadcrumb.jsx";
import LearningOutcomePanel from "../components/Commons/LearningOutcomePanel.jsx";
import Button from "../components/Commons/Button.jsx";
import PromptDialog from "../components/Commons/PromptDialog.jsx";

import useCurriculumAssessments from "../hooks/Curriculum_Hooks/useCurriculumAssessments.js";
import api from "../utils/api.js";

function AssessmentViewer() {
    const navigate = useNavigate();
    const location = useLocation();
    const { gradeId, courseId, unitId, chapterId } = useParams();

    const gradeName = location.state?.gradeName || `Grade ${gradeId}`;
    const courseName = location.state?.courseName || `Course ${courseId}`;
    const unitName = location.state?.unitName || `Unit ${unitId}`;
    const chapterNameFromState = location.state?.chapterName;

    const {
        curriculumId,
        chapterName,
        learningOutcomes,
        assessments,
        loading,
        error,
        refresh
    } = useCurriculumAssessments(gradeId, courseId, unitId, chapterId);

    const [actionLoading, setActionLoading] = useState(false);
    const [promptOpen, setPromptOpen] = useState(false);
    const [actionMessage, setActionMessage] = useState("");

    const displayChapterName = chapterNameFromState || chapterName || `Chapter ${chapterId}`;

    const handleViewAssessment = (assessmentId) => {
        console.log("[AssessmentViewer] Navigating to assessment editor:", assessmentId);
        navigate(`/view-assessment/${assessmentId}`, {
            state: {
                gradeId,
                courseId,
                unitId,
                chapterId,
                gradeName,
                courseName,
                unitName,
                chapterName: displayChapterName,
                curriculumId
            }
        });
    };

    const handleGenerateClick = () => {
        console.log("[AssessmentViewer] Generate assessment clicked. curriculumId:", curriculumId);
        setPromptOpen(true);
    };

    const handleGenerateConfirm = async (prompt) => {
        setPromptOpen(false);

        if (!curriculumId) {
            console.error("[AssessmentViewer] Cannot generate: missing curriculumId.");
            setActionMessage("Curriculum ID is missing. Cannot generate assessment.");
            return;
        }

        console.log("[AssessmentViewer] Generating assessment with prompt:", prompt);
        setActionLoading(true);
        setActionMessage("");

        try {
            const response = await api.generateAssesment(curriculumId, prompt);

            if (response.success) {
                console.log("[AssessmentViewer] Generate success:", response.message);
                setActionMessage(response.message || "Assessment generated successfully.");
                await refresh();
            } else {
                console.error("[AssessmentViewer] Generate failed:", response.message);
                setActionMessage(response.message);
            }
        } catch (err) {
            console.error("[AssessmentViewer] Generate error:", err);
            setActionMessage("Unable to generate assessment.");
        } finally {
            setActionLoading(false);
        }
    };

    const handleDeleteAssessment = async (assessmentId) => {
        console.log("[AssessmentViewer] Delete assessment clicked:", assessmentId);
        const confirmed = window.confirm("Are you sure you want to delete this assessment?");

        if (!confirmed) {
            console.log("[AssessmentViewer] Delete cancelled.");
            return;
        }

        setActionLoading(true);
        setActionMessage("");

        try {
            const response = await api.deleteAssessment(assessmentId);

            if (response.success) {
                console.log("[AssessmentViewer] Delete success:", response.message);
                setActionMessage(response.message || "Assessment deleted successfully.");
                await refresh();
            } else {
                console.error("[AssessmentViewer] Delete failed:", response.message);
                setActionMessage(response.message);
            }
        } catch (err) {
            console.error("[AssessmentViewer] Delete error:", err);
            setActionMessage("Unable to delete assessment.");
        } finally {
            setActionLoading(false);
        }
    };

    return (
        <div className="assessment-viewer">
            <CurriculumBreadcrumb
                items={[
                    { label: "Curriculum", to: "/" },
                    { label: gradeName, to: `/grades/${gradeId}/courses` },
                    {
                        label: courseName,
                        to: `/grades/${gradeId}/courses/${courseId}/units`
                    },
                    {
                        label: unitName,
                        to: `/grades/${gradeId}/courses/${courseId}/units/${unitId}/chapters`
                    },
                    { label: displayChapterName }
                ]}
            />

            <div className="page-header">
                <h1>{displayChapterName}</h1>
                <p>Generate, review and publish assessments for this chapter.</p>
            </div>

            <div className="learning-outcomes-section">
                <LearningOutcomePanel learningOutcomes={learningOutcomes} />
            </div>

            <div className="page-actions">
                <Button
                    text={actionLoading ? "Working..." : "+ Generate Assessment"}
                    onClick={handleGenerateClick}
                    disabled={actionLoading || loading || !curriculumId}
                />
            </div>

            {
                actionMessage && (
                    <div className="page-message">
                        {actionMessage}
                    </div>
                )
            }

            {
                loading ?
                    (
                        <div className="page-message">
                            <CircularProgress size={28} sx={{ mr: 1.5 }} />
                            Loading assessments...
                        </div>
                    )
                    : error ?
                        (
                            <div className="page-error">
                                {error}
                            </div>
                        )
                        : assessments.length === 0 ?
                            (
                                <div className="page-message">
                                    No assessments yet. Click Generate Assessment to create one.
                                </div>
                            )
                            : (
                                <div className="assessment-grid">
                                    {
                                        assessments.map((assessment) => (
                                            <AssesssmentCard
                                                key={assessment.assessmentId}
                                                assessment={assessment}
                                                onView={handleViewAssessment}
                                                onDelete={handleDeleteAssessment}
                                                disabled={actionLoading}
                                            />
                                        ))
                                    }
                                </div>
                            )
            }

            <PromptDialog
                open={promptOpen}
                title="Generate Assessment"
                label="Optional generation prompt"
                confirmText="Generate"
                onClose={() => {
                    console.log("[AssessmentViewer] Generate dialog closed.");
                    setPromptOpen(false);
                }}
                onConfirm={handleGenerateConfirm}
            />
        </div>
    );
}

export default AssessmentViewer;
