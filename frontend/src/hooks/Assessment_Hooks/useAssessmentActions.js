import { useState } from "react";
import api from "../../utils/api.js";

function useAssessmentActions(assessmentId) {

    const [loading, setLoading] = useState(false);

    const execute = async (label, apiCall) => {
        console.log(`[useAssessmentActions] Starting: ${label}`);
        setLoading(true);

        try {
            const response = await apiCall();
            console.log(`[useAssessmentActions] ${label} response:`, response);
            return response;
        } catch (error) {
            console.error(`[useAssessmentActions] ${label} failed:`, error);
            throw error;
        } finally {
            setLoading(false);
            console.log(`[useAssessmentActions] Finished: ${label}`);
        }
    };

    const regenerateAssessment = (prompt = "") =>
        execute("Regenerate Assessment", () => api.reGenerateAssesment(assessmentId, prompt));

    const generateDocument = () =>
        execute("Generate Document", () => api.generateDocument(assessmentId));

    const publishAssessment = () =>
        execute("Publish Assessment", () => api.publishAssessment(assessmentId));

    const rollbackAssessment = () =>
        execute("Rollback Assessment", () => api.rollBackAssesment(assessmentId));

    const deleteAssessment = () =>
        execute("Delete Assessment", () => api.deleteAssessment(assessmentId));

    const addQuestion = () =>
        execute("Add Question", () => api.addQuestion(assessmentId));

    return {
        loading,
        regenerateAssessment,
        generateDocument,
        publishAssessment,
        rollbackAssessment,
        deleteAssessment,
        addQuestion
    };
}

export default useAssessmentActions;
