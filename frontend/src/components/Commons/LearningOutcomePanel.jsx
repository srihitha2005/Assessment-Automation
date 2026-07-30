import { useState } from "react";
import "./styles/LearningOutcomePanel.css";
import { normalizeLearningOutcomes } from "../../utils/helper.js";

function LearningOutcomePanel({ learningOutcomes = [] }) {
    const [expanded, setExpanded] = useState(false);
    const outcomes = normalizeLearningOutcomes(learningOutcomes);

    const handleToggle = () => {
        console.log("[LearningOutcomePanel] Toggle:", !expanded, "count:", outcomes.length);
        setExpanded(!expanded);
    };

    return (
        <div className="learning-outcome-panel">
            <div
                className="learning-outcome-header"
                onClick={handleToggle}
            >
                <span className="learning-outcome-title">
                    Learning Outcomes
                </span>
                <button className="learning-outcome-button" type="button">
                    {outcomes.length} Learning Outcome
                    {outcomes.length !== 1 ? "s" : ""}
                    {expanded ? " ▲" : " ▼"}
                </button>
            </div>

            {
                expanded && (
                    <div className="learning-outcome-list">
                        {
                            outcomes.length === 0 ?
                                (
                                    <div className="learning-outcome-item">
                                        <span className="learning-outcome-description">
                                            No learning outcomes available.
                                        </span>
                                    </div>
                                )
                                :
                                outcomes.map((learningOutcome) => (
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
