import {useEffect, useState} from "react";
import api from "../utils/api.js";

const useAssessment = () => {
    const [assessments, setAssessments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchAssessments = async () => {
        try {
            setLoading(true);
            const response = await api.getAllAssessments();
            if (response.success) {
                setAssessments(response.data);
            }
            else {
                setError(response.message);
            }
        }
        catch {
            setError("Unable to fetch assessments.");
        }
        finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAssessments();
    }, []);

    return {
        assessments,
        loading,
        error,
        refresh: fetchAssessments
    };
};

export default useAssessment;