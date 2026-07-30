import { useEffect, useState } from "react";
import api from "../../utils/api.js";

const useChapters = (unitId) => {
    const [chapters, setChapters] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchChapters = async (id) => {
        if (!id) {
            console.warn("[useChapters] Missing unitId.");
            setLoading(false);
            return;
        }

        console.log("[useChapters] Loading chapters for unit:", id);

        try {
            setLoading(true);
            setError(null);

            const response = await api.getChaptersByUnit(id);

            if (response.success) {
                const chapterList = response.data?.chapters || [];
                console.log("[useChapters] Chapters loaded:", chapterList.length);
                setChapters(chapterList);
            } else {
                console.error("[useChapters]", response.message);
                setError(response.message);
            }
        } catch (err) {
            console.error("[useChapters] Failed to fetch chapters:", err);
            setError("Unable to fetch chapters.");
        } finally {
            setLoading(false);
            console.log("[useChapters] Loading complete.");
        }
    };

    useEffect(() => {
        fetchChapters(unitId);
    }, [unitId]);

    return {
        chapters,
        loading,
        error,
        refresh: fetchChapters
    };
};

export default useChapters;
