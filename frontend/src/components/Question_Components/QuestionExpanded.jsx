import "./styles/QuestionExpanded.css";

import QuestionMetadata from "./QuestionMetadata.jsx";
import QuestionToolbar from "./QuestionToolBar.jsx";

function QuestionExpanded({
                              question,
                              learningOutcomes,

                              isEditing,
                              onEdit,
                              onSave,
                              onCancel
                          }){

    return(
        <div className="question-expanded">
            <QuestionMetadata
                question={question}
                learningOutcomes={["LO1","LO2"]}
            />

            <QuestionToolbar
                question={question}
                isEditing={isEditing}
                onEdit={onEdit}
                onSave={onSave}
                onCancel={onCancel}
            />

        </div>

    );

}

export default QuestionExpanded;