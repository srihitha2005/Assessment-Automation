import "./styles/QuestionMetadata.css";

import LearningOutcomePanel from "../Commons/LearningOutcomePanel.jsx";
import { formatVersion, getDifficultyColor, getQuestionTypeBadgeColor, normalizeLearningOutcomes } from "../../utils/helper.js";

function QuestionMetadata({
    question,
    learningOutcomes
}) {
    const outcomes = Array.isArray(learningOutcomes) && learningOutcomes.length > 0
        ? normalizeLearningOutcomes(learningOutcomes)
        : normalizeLearningOutcomes(
            question.learningOutcome
                ? [question.learningOutcome]
                : []
        );

    return (
        <div className="question-metadata">
            <div className="question-metadata-row">
                <span className="question-metadata-label">
                    Question Type
                </span>

                <span
                    className="question-type-badge"
                    style={{
                        backgroundColor: getQuestionTypeBadgeColor(
                            question.questionType
                        )
                    }}
                >
                    {question.questionType || "-"}
                </span>
            </div>

            <LearningOutcomePanel
                learningOutcomes={outcomes}
            />

            <div className="question-metadata-row">
                <span className="question-metadata-label">
                    Marks
                </span>
                <span>
                    {question.marks ?? "-"}
                </span>
            </div>

            <div className="question-metadata-row">
                <span className="question-metadata-label">
                    Difficulty
                </span>
                <span
                    className="difficulty-badge"
                    style={{
                        backgroundColor: getDifficultyColor(
                            question.difficulty
                        )
                    }}
                >
                    {question.difficulty || "-"}
                </span>
            </div>

            <div className="question-metadata-row">
                <span className="question-metadata-label">
                    Bloom's Level
                </span>
                <span>
                    {question.bloomsLevel || question.bloomLevel || "-"}
                </span>
            </div>

            <div className="question-metadata-row">
                <span className="question-metadata-label">
                    Version
                </span>
                <span>
                    {formatVersion(question.version)}
                </span>
            </div>

            <div className="question-metadata-row">
                <span className="question-metadata-label">
                    Last Modified At
                </span>
                <span>
                    {question.lastModifiedAt || question.updatedOn || "-"}
                </span>
            </div>

            <div className="question-metadata-row">
                <span className="question-metadata-label">
                    Last Modified By
                </span>
                <span>
                    {question.lastModifiedBy || question.updatedBy || "-"}
                </span>
            </div>
        </div>
    );
}

export default QuestionMetadata;
