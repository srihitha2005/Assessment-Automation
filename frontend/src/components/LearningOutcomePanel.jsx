import { useState } from "react";
import "./LearningOutcomePanel.css";

function LearningOutcomePanel({ learningOutcomes }) {
    const [expanded, setExpanded] = useState(false);
    return (
        <div className="learning-outcome-panel">
            <div
                className="learning-outcome-header"
                onClick={() => setExpanded(!expanded)}
            >
                <span className="learning-outcome-title">
                    Learning Outcomes
                </span>
                <button className="learning-outcome-button">

                    {learningOutcomes.length} Learning Outcome
                    {learningOutcomes.length !== 1 ? "s" : ""}
                    {expanded ? " ▲" : " ▼"}
                </button>
            </div>

            {
                expanded && (
                    <div className="learning-outcome-list">
                        {
                            learningOutcomes.map((learningOutcome) => (
                                <div
                                    key={learningOutcome.learningOutcomeId}
                                    className="learning-outcome-item"
                                >
                                    <span className="learning-outcome-id">
                                        {learningOutcome.learningOutcomeId}
                                    </span>

                                    <span className="learning-outcome-description">
                                        {learningOutcome.description}
                                    </span>

                                </div>

                            ))

                        }

                    </div>

                )

            }

        </div>

    );

}

export default LearningOutcomePanel;