import { useState } from "react";
import api from "../utils/api.js";

function useQuestionToolbarActions() {
    const [loading, setLoading] = useState(false);
    const execute = async (apiCall) => {
        setLoading(true);
        try {
            return await apiCall();
        }
        finally {
            setLoading(false);
        }
    };

    const saveQuestion = (question) =>
        execute(() => api.updateQuestion(question));

    const regenerateQuestion = (questionId) =>
        execute(() => api.regenerateQuestion(questionId));

    const regenerateQuestionWithPrompt = (questionId) =>
        execute(() => api.regenerateQuestionWithPrompt(questionId));

    const rollbackQuestion = (questionId) =>
        execute(() => api.rollbackQuestion(questionId));

    const regenerateAnswer = (questionId) =>
        execute(() => api.regenerateAnswer(questionId));

    const uploadImages = (questionId, images) =>
        execute(() => api.uploadImage(questionId, images));

    const deleteImages = (questionId) =>
        execute(() => api.deleteImage(questionId));

    const deleteQuestion = (questionId) =>
        execute(() => api.deleteQuestion(questionId));

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