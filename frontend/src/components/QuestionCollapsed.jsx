import "./QuestionCollapsed.css";

import { QUESTION_TYPES } from "../utils/constants.js";
import {getDifficultyColor, getQuestionTypeBadgeColor} from "../utils/helper.js";

function QuestionCollapsed({

                               question,

                               expanded,
                               onToggle,

                               isEditing,

                               editedQuestion,
                               setEditedQuestion,

                               editedAnswer,
                               setEditedAnswer

                           }) {

    return (

        <div className="question-collapsed">

            <div
                className="question-header"
                onClick={onToggle}
            >

                <h3>

                    Question {question.questionNumber}

                </h3>

                <div className="question-badges">

                    <span className="marks-badge">

                        {question.marks} Marks

                    </span>

                    <span
                        className="question-type-badge"
                        style={{
                            backgroundColor:getQuestionTypeBadgeColor(question.questionType)
                        }}
                    >
                        {question.questionType}
                    </span>

                    <span
                        className="difficulty-badge"
                        style={{
                            backgroundColor:getDifficultyColor(question.difficulty)
                        }}
                    >
                        {question.difficulty}
                    </span>

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
                        onChange={(e)=>setEditedQuestion(e.target.value)}
                    />

                    :

                    <p className="question-text">

                        {question.question}

                    </p>
            }

            {

                question.images.length > 0 &&

                <div className="question-images">

                    {

                        question.images.map((image,index)=>(

                            <img

                                key={index}

                                src={image}

                                alt={`Question ${index+1}`}

                            />

                        ))

                    }

                </div>

            }

            {

                question.questionType===QUESTION_TYPES.MCQ &&

                <div className="question-options">

                    {

                        question.options.map((option,index)=>(

                            <div
                                key={index}
                                className="question-option"
                            >

                                {String.fromCharCode(65+index)}. {option}

                            </div>

                        ))

                    }

                </div>

            }

            {

                question.questionType===QUESTION_TYPES.TRUE_FALSE &&

                <div className="question-options">

                    <div>○ True</div>

                    <div>○ False</div>

                </div>

            }

            {

                isEditing ?

                    <textarea
                        className="answer-editor"
                        value={editedAnswer}
                        onChange={(e)=>setEditedAnswer(e.target.value)}
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