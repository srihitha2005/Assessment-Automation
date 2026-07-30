import { useState } from "react";
import api from "../../utils/api.js";
import useQuestions from "./useQuestions";

function useQuestionActions(assessmentId) {
    const [loading, setLoading] = useState(false);
    const { getQuestions } = useQuestions(assessmentId);
    const execute = async (apiCall) => {
        setLoading(true);
        try {
            const response = await apiCall();
            await getQuestions(assessmentId);
            return response;
        }
        finally {
            setLoading(false);
        }
    };

    const regenerateQuestion = (questionId) =>
        execute(() => api.regenerateQuestion());

    const updateQuestion = (question) =>
        execute(() => api.updateQuestion());

    const deleteQuestion = (questionId) =>
        execute(() => api.deleteQuestion());

    const addQuestion = () =>
        execute(() => api.addQuestion());

    const rollbackQuestion = (questionId) =>
        execute(() => api.rollbackQuestion());

    const generateAnswer = (questionId) =>
        execute(() => api.regenerateAnswer());

    const uploadImage = (questionId, image) =>
        execute(() => api.uploadImage());

    const parseImage = (questionId) =>
        execute(() => api.parseImage());

    return {
        loading,
        regenerateQuestion,
        updateQuestion,
        deleteQuestion,
        addQuestion,
        rollbackQuestion,
        generateAnswer,
        uploadImage,
        parseImage

    };

}

export default useQuestionActions;