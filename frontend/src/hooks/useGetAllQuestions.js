import {useEffect, useState} from "react";
import api from "../utils/api.js";

const useGetAllQuestions = (assessmentId) => {
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchQuestions = async (assessmentId) => {
        console.log("[useGetAllQuestions] Fetching questions for:", assessmentId);

        try {
            setLoading(true);
            const response = await api.getQuestionsByAssessment(assessmentId);

            if (response.success) {
                setQuestions(response.data);
                console.log("[useGetAllQuestions] Questions loaded:", response.data.length);
            }
            else {
                setError(response.message);
                console.error("[useGetAllQuestions]", response.message);
            }
        }
        catch (error) {
            setError("Unable to fetch questions.");
            console.error("[useGetAllQuestions] Failed to fetch questions:", error);
        }
        finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchQuestions(assessmentId);
    }, [assessmentId]);

    return {
        questions,
        loading,
        error,
        refresh: fetchQuestions
    };
};

export default useGetAllQuestions;
