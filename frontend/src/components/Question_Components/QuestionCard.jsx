import { useState } from "react";

import "./styles/QuestionCard.css";

import QuestionCollapsed from "./QuestionCollapsed.jsx";
import QuestionExpanded from "./QuestionExpanded.jsx";
import api from "../../utils/api.js";

function QuestionCard({
    question,
    learningOutcomes,
    onRefresh
}) {
    const [expanded, setExpanded] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [editedQuestion, setEditedQuestion] = useState(question.question);
    const [editedAnswer, setEditedAnswer] = useState(question.answer);
    const [editedOptions, setEditedOptions] = useState(question.options || []);
    const [message, setMessage] = useState("");

    const toggleExpanded = () => {
        console.log("[QuestionCard] Toggle expand for question:", question.questionId, !expanded);
        setExpanded(!expanded);
    };

    const handleEdit = () => {
        console.log("[QuestionCard] Edit clicked:", question.questionId);
        setEditedOptions(question.options || []);
        setIsEditing(true);
    };

    const handleSave = async () => {
        console.log("[QuestionCard] Save clicked:", question.questionId);
        setMessage("");

        try {
            const response = await api.updateQuestion(
                question.questionId,
                editedQuestion,
                editedAnswer
            );

            if (response.success) {
                console.log("[QuestionCard] Save success:", response.message);
                setMessage(response.message || "Question saved.");
                setIsEditing(false);
                if (onRefresh) {
                    await onRefresh();
                }
            } else {
                console.error("[QuestionCard] Save failed:", response.message);
                setMessage(response.message);
            }
        } catch (error) {
            console.error("[QuestionCard] Save error:", error);
            setMessage("Unable to save question.");
        }
    };

    const handleCancel = () => {
        console.log("[QuestionCard] Cancel edit:", question.questionId);
        setEditedQuestion(question.question);
        setEditedAnswer(question.answer);
        setEditedOptions(question.options || []);
        setIsEditing(false);
    };

    return (
        <div className="question-card">
            <QuestionCollapsed
                question={question}
                expanded={expanded}
                onToggle={toggleExpanded}
                isEditing={isEditing}
                editedQuestion={editedQuestion}
                setEditedQuestion={setEditedQuestion}
                editedAnswer={editedAnswer}
                setEditedAnswer={setEditedAnswer}
                editedOptions={editedOptions}
                setEditedOptions={setEditedOptions}
            />

            {
                expanded &&
                <QuestionExpanded
                    question={question}
                    learningOutcomes={learningOutcomes}
                    isEditing={isEditing}
                    onEdit={handleEdit}
                    onSave={handleSave}
                    onCancel={handleCancel}
                    onRefresh={onRefresh}
                    editedQuestion={editedQuestion}
                    editedAnswer={editedAnswer}
                />
            }

            {
                message && (
                    <p className="question-text" style={{ marginTop: "12px", color: "#2563EB" }}>
                        {message}
                    </p>
                )
            }
        </div>
    );
}

export default QuestionCard;
