import "./styles/QuestionToolBar.css";
import Button from "../Commons/Button.jsx";
import useQuestionToolbarActions from "../../hooks/Question_Hooks/useQuestionToolbarActions.js";

function QuestionToolbar({

                             question,
                             isEditing,

                             onEdit,
                             onSave,
                             onCancel

                         }) {

    const {

        loading,

        saveQuestion,

        regenerateQuestion,
        regenerateQuestionWithPrompt,
        rollbackQuestion,

        regenerateAnswer,

        uploadImages,
        deleteImages,

        deleteQuestion

    } = useQuestionToolbarActions();

    return (

        <div className="question-toolbar">

            <div className="question-toolbar-row">

                {

                    isEditing ?

                        <>

                            <Button
                                text="Save"
                                onClick={() => {
                                    saveQuestion(question);
                                    onSave();
                                }}
                                disabled={loading}
                            />

                            <Button
                                text="Cancel"
                                onClick={onCancel}
                                disabled={loading}
                            />

                        </>

                        :

                        <>

                            <Button
                                text="Edit"
                                onClick={onEdit}
                                disabled={loading}
                            />

                            <Button
                                text="Regenerate"
                                onClick={() => regenerateQuestion(question.questionId)}
                                disabled={loading}
                            />

                            <Button
                                text="Regenerate with Prompt"
                                onClick={() => regenerateQuestionWithPrompt(question.questionId)}
                                disabled={loading}
                            />

                            <Button
                                text="Rollback"
                                onClick={() => rollbackQuestion(question.questionId)}
                                disabled={loading}
                            />

                        </>

                }

            </div>

            <div className="question-toolbar-row">

                <Button
                    text="Regenerate Answer"
                    onClick={() => regenerateAnswer(question.questionId)}
                    disabled={loading}
                />

            </div>

            <div className="question-toolbar-row">

                <Button
                    text="Upload Image(s)"
                    onClick={() => uploadImages(question.questionId)}
                    disabled={loading}
                />

                <Button
                    text="Delete Image(s)"
                    onClick={() => deleteImages(question.questionId)}
                    disabled={loading}
                />

            </div>

            <div className="question-toolbar-row question-toolbar-danger">

                <Button
                    text="Delete"
                    onClick={() => deleteQuestion(question.questionId)}
                    disabled={loading}
                />

            </div>

        </div>

    );

}

export default QuestionToolbar;