import { useEffect, useState } from "react";
import api from "../../utils/api.js";

const useUnits = (gradeId, courseId) => {
    const [units, setUnits] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchUnits = async (gid, cid) => {
        if (!cid || !gid) {
            console.warn("[useUnits] Missing courseId or gradeId.");
            setLoading(false);
            return;
        }

        console.log("[useUnits] Loading units for grade:", gid, "course:", cid);

        try {
            setLoading(true);
            setError(null);

            const response = await api.getUnitsByCourse(gid, cid);

            if (response.success) {
                const unitList = response.data?.units || [];
                console.log("[useUnits] Units loaded:", unitList.length);
                setUnits(unitList);
            } else {
                console.error("[useUnits]", response.message);
                setError(response.message);
            }
        } catch (err) {
            console.error("[useUnits] Failed to fetch units:", err);
            setError("Unable to fetch units.");
        } finally {
            setLoading(false);
            console.log("[useUnits] Loading complete.");
        }
    };

    useEffect(() => {
        fetchUnits(gradeId, courseId);
    }, [gradeId, courseId]);

    return {
        units,
        loading,
        error,
        refresh: fetchUnits
    };
};

export default useUnits;
