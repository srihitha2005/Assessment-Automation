import { useEffect, useState } from "react";
import api from "../../utils/api.js";

const useGrades = () => {
    const [grades, setGrades] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchGrades = async () => {
        console.log("[useGrades] Loading grades...");
        try {
            setLoading(true);
            setError(null);

            const response = await api.getAllGrades();

            if (response.success) {
                const gradeList = response.data?.grades || [];
                console.log("[useGrades] Grades loaded:", gradeList.length);
                setGrades(gradeList);
            } else {
                console.error("[useGrades]", response.message);
                setError(response.message);
            }
        } catch (err) {
            console.error("[useGrades] Failed to fetch grades:", err);
            setError("Unable to fetch grades.");
        } finally {
            setLoading(false);
            console.log("[useGrades] Loading complete.");
        }
    };

    useEffect(() => {
        fetchGrades();
    }, []);

    return {
        grades,
        loading,
        error,
        refresh: fetchGrades
    };
};

export default useGrades;
