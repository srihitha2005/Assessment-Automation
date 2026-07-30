import "./styles/QuestionCollapsed.css";

import { QUESTION_TYPES } from "../../utils/constants.js";
import { getDifficultyColor, getQuestionTypeBadgeColor, hasImages } from "../../utils/helper.js";

function QuestionCollapsed({
    question,
    expanded,
    onToggle,
    isEditing,
    editedQuestion,
    setEditedQuestion,
    editedAnswer,
    setEditedAnswer,
    editedOptions = [],
    setEditedOptions
}) {
    const options = isEditing ? (editedOptions || []) : (question.options || []);
    const images = question.images || [];

    const handleOptionChange = (index, value) => {
        console.log("[QuestionCollapsed] Option edited:", index, value);
        const updatedOptions = [...options];
        updatedOptions[index] = value;
        setEditedOptions?.(updatedOptions);
    };

    return (
        <div className="question-collapsed">
            <div
                className="question-header"
                onClick={onToggle}
            >
                <h3>
                    Question {question.questionNumber ?? question.questionId}
                </h3>

                <div className="question-badges">
                    <span className="marks-badge">
                        {question.marks ?? "-"} Marks
                    </span>

                    {
                        question.questionType && (
                            <span
                                className="question-type-badge"
                                style={{
                                    backgroundColor: getQuestionTypeBadgeColor(question.questionType)
                                }}
                            >
                                {question.questionType}
                            </span>
                        )
                    }

                    {
                        question.difficulty && (
                            <span
                                className="difficulty-badge"
                                style={{
                                    backgroundColor: getDifficultyColor(question.difficulty)
                                }}
                            >
                                {question.difficulty}
                            </span>
                        )
                    }

                    <span className="expand-icon">
                        {expanded ? "▲" : "▼"}
                    </span>
                </div>
            </div>

            {
                isEditing ?
                    <textarea
                        className="question-editor"
                        value={editedQuestion}
                        onChange={(e) => setEditedQuestion(e.target.value)}
                    />
                    :
                    <p className="question-text">
                        {question.question}
                    </p>
            }

            {
                hasImages(question) &&
                <div className="question-images">
                    {
                        images.map((image, index) => (
                            <img
                                key={image.imageId || index}
                                src={image.imagePath || image}
                                alt={`Question ${index + 1}`}
                            />
                        ))
                    }
                </div>
            }

            {
                question.questionType === QUESTION_TYPES.MCQ &&
                <div className="question-options">
                    {
                        options.map((option, index) => (
                            <div
                                key={index}
                                className="question-option"
                            >
                                {
                                    isEditing ?
                                        (
                                            <div className="option-editor-row">
                                                <span>{String.fromCharCode(65 + index)}.</span>
                                                <input
                                                    className="option-editor"
                                                    type="text"
                                                    value={option}
                                                    onChange={(e) => handleOptionChange(index, e.target.value)}
                                                />
                                            </div>
                                        )
                                        :
                                        (
                                            <>
                                                {String.fromCharCode(65 + index)}. {option}
                                            </>
                                        )
                                }
                            </div>
                        ))
                    }
                </div>
            }

            {
                question.questionType === QUESTION_TYPES.TRUE_FALSE &&
                <div className="question-options">
                    {
                        isEditing ?
                            (
                                <>
                                    <div className="question-option">
                                        <div className="option-editor-row">
                                            <span>A.</span>
                                            <input
                                                className="option-editor"
                                                type="text"
                                                value={options[0] ?? "True"}
                                                onChange={(e) => handleOptionChange(0, e.target.value)}
                                            />
                                        </div>
                                    </div>
                                    <div className="question-option">
                                        <div className="option-editor-row">
                                            <span>B.</span>
                                            <input
                                                className="option-editor"
                                                type="text"
                                                value={options[1] ?? "False"}
                                                onChange={(e) => handleOptionChange(1, e.target.value)}
                                            />
                                        </div>
                                    </div>
                                </>
                            )
                            :
                            (
                                <>
                                    <div>○ True</div>
                                    <div>○ False</div>
                                </>
                            )
                    }
                </div>
            }

            {
                isEditing ?
                    <textarea
                        className="answer-editor"
                        value={editedAnswer}
                        onChange={(e) => setEditedAnswer(e.target.value)}
                    />
                    :
                    <div className="question-answer">
                        <strong>Answer</strong>
                        <p>
                            {question.answer}
                        </p>
                    </div>
            }
        </div>
    );
}

export default QuestionCollapsed;
