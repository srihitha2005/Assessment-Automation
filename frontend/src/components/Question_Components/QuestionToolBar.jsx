import "./styles/QuestionToolBar.css";

import { useRef, useState } from "react";

import Button from "../Commons/Button.jsx";
import PromptDialog from "../Commons/PromptDialog.jsx";
import useQuestionToolbarActions from "../../hooks/Question_Hooks/useQuestionToolbarActions.js";

function QuestionToolbar({
    question,
    isEditing,
    onEdit,
    onSave,
    onCancel,
    onRefresh
}) {
    const fileInputRef = useRef(null);
    const [promptOpen, setPromptOpen] = useState(false);
    const [promptMode, setPromptMode] = useState(null);
    const [message, setMessage] = useState("");

    const {
        loading,
        regenerateQuestion,
        regenerateQuestionWithPrompt,
        rollbackQuestion,
        regenerateAnswer,
        uploadImages,
        deleteImages,
        deleteQuestion
    } = useQuestionToolbarActions(onRefresh);

    const runAction = async (label, action) => {
        console.log(`[QuestionToolbar] ${label} clicked:`, question.questionId);
        setMessage("");

        try {
            const response = await action();
            if (response?.success === false) {
                console.error(`[QuestionToolbar] ${label} failed:`, response.message);
                setMessage(response.message);
                return;
            }
            console.log(`[QuestionToolbar] ${label} success:`, response);
            setMessage(response?.message || `${label} completed.`);
        } catch (error) {
            console.error(`[QuestionToolbar] ${label} error:`, error);
            setMessage(`${label} failed.`);
        }
    };

    const openPrompt = (mode) => {
        console.log("[QuestionToolbar] Opening prompt for:", mode);
        setPromptMode(mode);
        setPromptOpen(true);
    };

    const handlePromptConfirm = async (prompt) => {
        setPromptOpen(false);

        if (promptMode === "question") {
            await runAction("Regenerate with Prompt", () =>
                regenerateQuestionWithPrompt(question.questionId, prompt)
            );
        }

        if (promptMode === "answer") {
            await runAction("Regenerate Answer", () =>
                regenerateAnswer(question.questionId, prompt)
            );
        }

        setPromptMode(null);
    };

    const handleUploadClick = () => {
        console.log("[QuestionToolbar] Upload image(s) clicked:", question.questionId);
        fileInputRef.current?.click();
    };

    const handleFilesSelected = async (event) => {
        const files = Array.from(event.target.files || []);
        console.log("[QuestionToolbar] Files selected:", files.length);

        if (files.length === 0) {
            return;
        }

        await runAction("Upload Images", () => uploadImages(question.questionId, files));
        event.target.value = "";
    };

    const handleDeleteImages = async () => {
        const firstImage = (question.images || [])[0];
        const imageId = firstImage?.imageId;

        if (!imageId) {
            console.warn("[QuestionToolbar] No image ID available to delete.");
            setMessage("No image available to delete.");
            return;
        }

        await runAction("Delete Images", () => deleteImages(imageId));
    };

    const handleDeleteQuestion = async () => {
        const confirmed = window.confirm("Delete this question?");
        if (!confirmed) {
            console.log("[QuestionToolbar] Delete question cancelled.");
            return;
        }
        await runAction("Delete Question", () => deleteQuestion(question.questionId));
    };

    return (
        <div className="question-toolbar">
            <div className="question-toolbar-row">
                {
                    isEditing ?
                        <>
                            <Button
                                text="Save"
                                onClick={onSave}
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
                                onClick={() =>
                                    runAction("Regenerate", () =>
                                        regenerateQuestion(question.questionId)
                                    )
                                }
                                disabled={loading}
                            />
                            <Button
                                text="Regenerate with Prompt"
                                onClick={() => openPrompt("question")}
                                disabled={loading}
                            />
                            <Button
                                text="Rollback"
                                onClick={() =>
                                    runAction("Rollback", () =>
                                        rollbackQuestion(question.questionId)
                                    )
                                }
                                disabled={loading}
                            />
                        </>
                }
            </div>

            <div className="question-toolbar-row">
                <Button
                    text="Regenerate Answer"
                    onClick={() => openPrompt("answer")}
                    disabled={loading}
                />
            </div>

            <div className="question-toolbar-row">
                <Button
                    text="Upload Image(s)"
                    onClick={handleUploadClick}
                    disabled={loading}
                />
                <Button
                    text="Delete Image(s)"
                    onClick={handleDeleteImages}
                    disabled={loading}
                />
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    multiple
                    style={{ display: "none" }}
                    onChange={handleFilesSelected}
                />
            </div>

            <div className="question-toolbar-row question-toolbar-danger">
                <Button
                    text="Delete"
                    onClick={handleDeleteQuestion}
                    disabled={loading}
                />
            </div>

            {
                message && (
                    <p style={{ color: "#2563EB", margin: 0 }}>
                        {message}
                    </p>
                )
            }

            <PromptDialog
                open={promptOpen}
                title={promptMode === "answer" ? "Regenerate Answer" : "Regenerate Question"}
                label="Optional prompt"
                confirmText="Regenerate"
                onClose={() => {
                    console.log("[QuestionToolbar] Prompt dialog closed.");
                    setPromptOpen(false);
                    setPromptMode(null);
                }}
                onConfirm={handlePromptConfirm}
            />
        </div>
    );
}

export default QuestionToolbar;
