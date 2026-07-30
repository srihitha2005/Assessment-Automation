import "./styles/AssessmentCard.css";
import Button from "../Commons/Button.jsx";
import {
    formatVersion,
    getLearningOutcomeCount,
    getStatusColor,
} from "../../utils/helper.js";

function AssesssmentCard({ assessment = {}, onView, onDelete, disabled = false }) {
    const {
        assessmentId,
        assessmentNumber,
        chapterName,
        learningOutcomes,
        marks,
        questionCount,
        numberOfQuestions,
        status,
        version,
    } = assessment;

    const questions = questionCount ?? numberOfQuestions;

    const handleView = () => {
        if (assessmentId == null) {
            console.error("[AssessmentCard] Cannot view assessment: missing assessment ID.", {
                status,
            });
            return;
        }

        console.log("[AssessmentCard] View assessment:", assessmentId);

        try {
            onView(assessmentId);
        } catch (error) {
            console.error("[AssessmentCard] Failed to open assessment.", {
                assessmentId,
                error,
            });
            throw error;
        }
    };

    const handleDelete = () => {
        if (assessmentId == null) {
            console.error("[AssessmentCard] Cannot delete assessment: missing assessment ID.");
            return;
        }

        console.log("[AssessmentCard] Delete assessment:", assessmentId);
        onDelete?.(assessmentId);
    };

    return (
        <div className="assessment-card">
            <div className="assessment-header">
                <div>
                    <h2>
                        Assessment {assessmentNumber ?? assessmentId ?? "--"}
                        {chapterName ? `: ${chapterName}` : ""}
                    </h2>
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
                    {questions ?? "--"}
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
                <Button
                    text="Delete"
                    onClick={handleDelete}
                    disabled={disabled}
                />
                <Button
                    text="View Assessment"
                    onClick={handleView}
                    disabled={disabled}
                />
            </div>
        </div>
    );
}

export default AssesssmentCard;
