import { useEffect, useState } from "react";
import api from "../../utils/api.js";

const useCourses = (gradeId) => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchCourses = async (id) => {
        if (!id) {
            console.warn("[useCourses] Missing gradeId.");
            setLoading(false);
            return;
        }

        console.log("[useCourses] Loading courses for grade:", id);

        try {
            setLoading(true);
            setError(null);

            const response = await api.getCoursesByGrade(id);

            if (response.success) {
                const courseList = response.data?.courses || [];
                console.log("[useCourses] Courses loaded:", courseList.length);
                setCourses(courseList);
            } else {
                console.error("[useCourses]", response.message);
                setError(response.message);
            }
        } catch (err) {
            console.error("[useCourses] Failed to fetch courses:", err);
            setError("Unable to fetch courses.");
        } finally {
            setLoading(false);
            console.log("[useCourses] Loading complete.");
        }
    };

    useEffect(() => {
        fetchCourses(gradeId);
    }, [gradeId]);

    return {
        courses,
        loading,
        error,
        refresh: fetchCourses
    };
};

export default useCourses;
