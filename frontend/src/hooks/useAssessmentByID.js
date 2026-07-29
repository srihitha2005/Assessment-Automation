import {useEffect, useState} from "react";
import api from "../utils/api.js";

const useAssessmentByID = (assessmentId) => {
    const [assessment, setAssessment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchAssessmentByID = async (assessmentId) => {
        console.log("[useAssessmentByID] Fetching assessment:", assessmentId);

        try {
            setLoading(true);
            const response = await api.getAssessmentsByID(assessmentId);

            if (response.success) {
                setAssessment(response.data);
                console.log("[useAssessmentByID] Assessment loaded:", response.data.assessmentId);
            }
            else {
                setError(response.message);
                console.error("[useAssessmentByID]", response.message);
            }
        }
        catch (error) {
            setError("Unable to fetch assessments.");
            console.error("[useAssessmentByID] Failed to fetch assessment:", error);
        }
        finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAssessmentByID(assessmentId);
    }, [assessmentId]);

    return {
        assessment,
        loading,
        error,
        refresh: fetchAssessmentByID
    };
};

export default useAssessmentByID;
