import "./AssessmentViewer.css";
import AssesssmentCard from "../components/AssesssmentCard.jsx";
import useAssessment from "../hooks/useAssessment.js";
import { useNavigate } from "react-router-dom";

function AssessmentViewer() {
    const navigate = useNavigate();

    const {
        assessments,
        loading,
        error
    } = useAssessment();

    const handleViewAssessment = (assessmentId) => {
        console.log("[AssessmentViewer] About to navigate:", assessmentId);

        navigate(`/view-assessment/${assessmentId}`);

        console.log("[AssessmentViewer] navigate() called");
    };

    return (
        <div className="assessment-viewer">
            <div className="page-header">
                <h1>
                    Assessments
                </h1>
                <p>
                    Generate, review and publish assessments.
                </p>
            </div>

            {
                loading ?
                    (
                        <div className="page-message">
                            Loading assessments...
                        </div>
                    )
                    : error ?
                        (
                            <div className="page-error">
                                {error}
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
                                        />
                                    ))
                                }
                            </div>
                        )
            }
        </div>
    );
}

export default AssessmentViewer;
