import "./styles/QuestionExpanded.css";

import QuestionMetadata from "./QuestionMetadata.jsx";
import QuestionToolbar from "./QuestionToolBar.jsx";

function QuestionExpanded({
    question,
    learningOutcomes,
    isEditing,
    onEdit,
    onSave,
    onCancel,
    onRefresh,
    editedQuestion,
    editedAnswer
}) {
    return (
        <div className="question-expanded">
            <QuestionMetadata
                question={question}
                learningOutcomes={learningOutcomes}
            />

            <QuestionToolbar
                question={question}
                isEditing={isEditing}
                onEdit={onEdit}
                onSave={onSave}
                onCancel={onCancel}
                onRefresh={onRefresh}
                editedQuestion={editedQuestion}
                editedAnswer={editedAnswer}
            />
        </div>
    );
}

export default QuestionExpanded;
