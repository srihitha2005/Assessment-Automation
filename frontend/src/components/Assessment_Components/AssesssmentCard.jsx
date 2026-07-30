import "./styles/AssessmentCard.css";
import Button from "../Commons/Button.jsx";
import {
    formatVersion,
    getLearningOutcomeCount,
    getStatusColor,
} from "../../utils/helper.js";

function AssesssmentCard({ assessment = {}, onView }) {
    const {
        assessmentId,
        chapterName,
        learningOutcomes,
        marks,
        questionCount,
        status,
        version,
    } = assessment;

    const handleView = () => {
        if (assessmentId == null) {
            console.error("[AssessmentCard] Cannot view assessment: missing assessment ID.", {
                status,
            });
            return;
        }

        console.log("[AssessmentCard] View assessment logggg:", assessmentId);

        try {
            onView(assessmentId);
        } catch (error) {
            console.error("[AssessmentCard] Failed to open assessment.", {
                assessmentId,
                error,
            });
            throw error;
        }

        console.log("After onView, {}", assessmentId);
    };

    return (
        <div className="assessment-card">
            <div className="assessment-header">
                <div>
                    <h2>Assessment {assessmentId ?? "--"}: {chapterName || "Untitled"}</h2>
                </div>

                <div
                    className="status-badge"
                    style={{
                        background: getStatusColor(status),
                    }}
                >
                    {status || "Unknown"}
                </div>
            </div>

            <div className="assessment-details">
                <div>
                    <strong>Learning Outcomes</strong>
                    <br />
                    {getLearningOutcomeCount(learningOutcomes)}
                </div>

                <div>
                    <strong>Questions</strong>
                    <br />
                    {questionCount ?? "--"}
                </div>

                <div>
                    <strong>Marks</strong>
                    <br />
                    {marks ?? "--"}
                </div>

                <div>
                    <strong>Version</strong>
                    <br />
                    {formatVersion(version)}
                </div>
            </div>

            <div className="assessment-footer">
                <Button text="View Assessment" onClick={handleView} />
            </div>
        </div>
    );
}

export default AssesssmentCard;
