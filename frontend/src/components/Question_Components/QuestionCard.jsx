import { useState } from "react";

import "./styles/QuestionCard.css";

import QuestionCollapsed from "./QuestionCollapsed.jsx";
import QuestionExpanded from "./QuestionExpanded.jsx";

function QuestionCard({

                          question,
                          learningOutcomes

                      }){

    const [expanded,setExpanded]=useState(false);

    const [isEditing,setIsEditing]=useState(false);

    const [editedQuestion,setEditedQuestion]=useState(question.question);

    const [editedAnswer,setEditedAnswer]=useState(question.answer);

    const toggleExpanded=()=>{

        setExpanded(!expanded);

    };

    const handleEdit=()=>{

        setIsEditing(true);

    };

    const handleSave=()=>{

        //TODO
        //Backend integration

        setIsEditing(false);

    };

    const handleCancel=()=>{

        setEditedQuestion(question.question);

        setEditedAnswer(question.answer);

        setIsEditing(false);

    };

    return(

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

                />

            }

        </div>

    );

}

export default QuestionCard;