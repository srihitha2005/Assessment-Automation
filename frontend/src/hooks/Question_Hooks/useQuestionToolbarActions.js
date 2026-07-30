import { useState } from "react";
import api from "../../utils/api.js";

function useQuestionToolbarActions(onRefresh) {
    const [loading, setLoading] = useState(false);

    const execute = async (label, apiCall) => {
        console.log(`[useQuestionToolbarActions] Starting: ${label}`);
        setLoading(true);

        try {
            const response = await apiCall();
            console.log(`[useQuestionToolbarActions] ${label} response:`, response);

            if (onRefresh) {
                await onRefresh();
            }

            return response;
        } catch (error) {
            console.error(`[useQuestionToolbarActions] ${label} failed:`, error);
            throw error;
        } finally {
            setLoading(false);
            console.log(`[useQuestionToolbarActions] Finished: ${label}`);
        }
    };

    const saveQuestion = (questionId, questionText, answer) =>
        execute("Save Question", () => api.updateQuestion(questionId, questionText, answer));

    const regenerateQuestion = (questionId, prompt = "") =>
        execute("Regenerate Question", () => api.regenerateQuestion(questionId, prompt));

    const regenerateQuestionWithPrompt = (questionId, prompt = "") =>
        execute("Regenerate Question With Prompt", () => api.regenerateQuestion(questionId, prompt));

    const rollbackQuestion = (questionId) =>
        execute("Rollback Question", () => api.rollbackQuestion(questionId));

    const regenerateAnswer = (questionId, prompt = "") =>
        execute("Regenerate Answer", () => api.regenerateAnswer(questionId, prompt));

    const uploadImages = (questionId, images) =>
        execute("Upload Images", () => api.uploadImage(questionId, images));

    const deleteImages = (imageId) =>
        execute("Delete Image", () => api.deleteImage(imageId));

    const deleteQuestion = (questionId) =>
        execute("Delete Question", () => api.deleteQuestion(questionId));

    return {
        loading,
        saveQuestion,
        regenerateQuestion,
        regenerateQuestionWithPrompt,
        rollbackQuestion,
        regenerateAnswer,
        uploadImages,
        deleteImages,
        deleteQuestion
    };
}

export default useQuestionToolbarActions;
