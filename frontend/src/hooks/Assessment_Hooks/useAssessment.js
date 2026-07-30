import {useEffect, useState} from "react";
import api from "../../utils/api.js";

const useAssessment = (curriculumId) => {
    const [assessments, setAssessments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchAssessments = async (id = curriculumId) => {
        if (!id) {
            console.warn("[useAssessment] Missing curriculumId.");
            setLoading(false);
            return;
        }

        console.log("[useAssessment] Fetching assessments for curriculum:", id);

        try {
            setLoading(true);
            const response = await api.getAllAssessments(id);

            if (response.success) {
                const data = response.data || {};
                const chapterName = data["Chapter Name"] || data.chapterName || "";
                const assessmentList = (data.assessments || []).map((assessment) => ({
                    ...assessment,
                    chapterName,
                    questionCount: assessment.numberOfQuestions ?? assessment.questionCount,
                    learningOutcomes: data.learningOutcomes || []
                }));

                console.log("[useAssessment] Assessments loaded:", assessmentList.length);
                setAssessments(assessmentList);
            }
            else {
                console.error("[useAssessment]", response.message);
                setError(response.message);
            }
        }
        catch (err) {
            console.error("[useAssessment] Failed:", err);
            setError("Unable to fetch assessments.");
        }
        finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAssessments();
    }, [curriculumId]);

    return {
        assessments,
        loading,
        error,
        refresh: fetchAssessments
    };
};

export default useAssessment;
