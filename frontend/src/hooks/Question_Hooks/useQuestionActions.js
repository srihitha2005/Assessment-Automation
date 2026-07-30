import { useState } from "react";
import api from "../../utils/api.js";

function useQuestionActions(assessmentId, refreshQuestions) {
    const [loading, setLoading] = useState(false);

    const execute = async (label, apiCall) => {
        console.log(`[useQuestionActions] Starting: ${label}`);
        setLoading(true);

        try {
            const response = await apiCall();
            console.log(`[useQuestionActions] ${label} response:`, response);

            if (refreshQuestions && assessmentId) {
                await refreshQuestions(assessmentId);
            }

            return response;
        } catch (error) {
            console.error(`[useQuestionActions] ${label} failed:`, error);
            throw error;
        } finally {
            setLoading(false);
        }
    };

    const regenerateQuestion = (questionId, prompt = "") =>
        execute("Regenerate Question", () => api.regenerateQuestion(questionId, prompt));

    const updateQuestion = (questionId, question, answer) =>
        execute("Update Question", () => api.updateQuestion(questionId, question, answer));

    const deleteQuestion = (questionId) =>
        execute("Delete Question", () => api.deleteQuestion(questionId));

    const addQuestion = () =>
        execute("Add Question", () => api.addQuestion(assessmentId));

    const rollbackQuestion = (questionId) =>
        execute("Rollback Question", () => api.rollbackQuestion(questionId));

    const generateAnswer = (questionId, prompt = "") =>
        execute("Regenerate Answer", () => api.regenerateAnswer(questionId, prompt));

    const uploadImage = (questionId, image) =>
        execute("Upload Image", () => api.uploadImage(questionId, image));

    return {
        loading,
        regenerateQuestion,
        updateQuestion,
        deleteQuestion,
        addQuestion,
        rollbackQuestion,
        generateAnswer,
        uploadImage
    };
}

export default useQuestionActions;
