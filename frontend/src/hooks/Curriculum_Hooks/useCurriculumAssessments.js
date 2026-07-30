import { useEffect, useState } from "react";
import api from "../../utils/api.js";
import { normalizeLearningOutcomes } from "../../utils/helper.js";

const useCurriculumAssessments = (gradeId, courseId, unitId, chapterId) => {
    const [curriculumId, setCurriculumId] = useState(null);
    const [chapterName, setChapterName] = useState("");
    const [learningOutcomes, setLearningOutcomes] = useState([]);
    const [assessments, setAssessments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchAssessments = async () => {
        if (!gradeId || !courseId || !unitId || !chapterId) {
            console.warn("[useCurriculumAssessments] Missing curriculum path params.");
            setLoading(false);
            return;
        }

        console.log("[useCurriculumAssessments] Resolving curriculum:", {
            gradeId,
            courseId,
            unitId,
            chapterId
        });

        try {
            setLoading(true);
            setError(null);

            const curriculumResponse = await api.getCurriculumId(
                gradeId,
                courseId,
                unitId,
                chapterId
            );

            if (!curriculumResponse.success) {
                console.error("[useCurriculumAssessments]", curriculumResponse.message);
                setError(curriculumResponse.message);
                return;
            }

            const resolvedCurriculumId = curriculumResponse.data?.curriculumId;
            console.log("[useCurriculumAssessments] Curriculum ID:", resolvedCurriculumId);
            setCurriculumId(resolvedCurriculumId);

            const assessmentsResponse = await api.getAssessmentsByCurriculum(resolvedCurriculumId);

            if (!assessmentsResponse.success) {
                console.error("[useCurriculumAssessments]", assessmentsResponse.message);
                setError(assessmentsResponse.message);
                return;
            }

            const data = assessmentsResponse.data || {};
            const chapterLabel = data["Chapter Name"] || data.chapterName || "Chapter";
            const outcomes = normalizeLearningOutcomes(data.learningOutcomes || []);
            const assessmentList = (data.assessments || []).map((assessment) => ({
                ...assessment,
                chapterName: chapterLabel,
                questionCount: assessment.numberOfQuestions ?? assessment.questionCount,
                learningOutcomes: outcomes,
                learningOutcomeCount: outcomes.length,
                version: assessment.version ?? null
            }));

            console.log("[useCurriculumAssessments] Assessments loaded:", assessmentList.length);
            setChapterName(chapterLabel);
            setLearningOutcomes(outcomes);
            setAssessments(assessmentList);
        } catch (err) {
            console.error("[useCurriculumAssessments] Failed:", err);
            setError("Unable to fetch assessments.");
        } finally {
            setLoading(false);
            console.log("[useCurriculumAssessments] Loading complete.");
        }
    };

    useEffect(() => {
        fetchAssessments();
    }, [gradeId, courseId, unitId, chapterId]);

    return {
        curriculumId,
        chapterName,
        learningOutcomes,
        assessments,
        loading,
        error,
        refresh: fetchAssessments
    };
};

export default useCurriculumAssessments;
