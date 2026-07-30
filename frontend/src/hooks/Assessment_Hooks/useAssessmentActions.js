import { useState } from "react";
import api from "../../utils/api.js";
import useGetAllQuestions from "../Question_Hooks/useGetAllQuestions.js";

function useAssessmentActions(assessmentId) {

    const [loading, setLoading] = useState(false);

    const { refresh } = useGetAllQuestions(assessmentId);

    const execute = async (apiCall) => {

        setLoading(true);

        try {

            const response = await apiCall();

            await refresh();

            return response;

        } catch (error) {

            console.error("[useAssessmentActions]", error);
            throw error;

        } finally {

            setLoading(false);

        }

    };

    const generateAssessment = () =>
        execute(() => api.generateAssesment());

    const regenerateAssessment = () =>
        execute(() => api.reGenerateAssesment());

    const generateDocument = () =>
        execute(() => api.generateDocument(assessmentId));

    const publishAssessment = () =>
        execute(() => api.publishAssessment());

    const rollbackAssessment = () =>
        execute(() => api.rollBackAssesment());

    const deleteAssessment = () =>
        execute(() => api.deleteAssessment());

    const addQuestion = () =>
        execute(() => api.addQuestion());

    const parseAssessment = () =>
        execute(() => api.parseAssesment());

    return {

        loading,

        generateAssessment,
        regenerateAssessment,
        generateDocument,
        publishAssessment,
        rollbackAssessment,
        deleteAssessment,
        addQuestion,
        parseAssessment

    };

}

export default useAssessmentActions;