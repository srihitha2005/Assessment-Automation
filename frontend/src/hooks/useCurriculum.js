import { useQuery } from "@tanstack/react-query";

import { curriculumApi, plannerApi } from "../lib/api.js";

export const useGrades = () =>
    useQuery({ queryKey: ["curriculum", "grades"], queryFn: curriculumApi.grades });

export const useCourses = (gradeId) =>
    useQuery({
        queryKey: ["curriculum", "grades", gradeId, "courses"],
        queryFn: () => curriculumApi.coursesByGrade(gradeId),
        enabled: Boolean(gradeId),
    });

export const useUnits = (courseId) =>
    useQuery({
        queryKey: ["curriculum", "courses", courseId, "units"],
        queryFn: () => curriculumApi.unitsByCourse(courseId),
        enabled: Boolean(courseId),
    });

export const useChapters = (unitId) =>
    useQuery({
        queryKey: ["curriculum", "units", unitId, "chapters"],
        queryFn: () => curriculumApi.chaptersByUnit(unitId),
        enabled: Boolean(unitId),
    });

export const usePlanners = () =>
    useQuery({ queryKey: ["planners"], queryFn: plannerApi.all });

export const usePlanner = (plannerId) =>
    useQuery({
        queryKey: ["planners", plannerId],
        queryFn: () => plannerApi.byId(plannerId),
        enabled: Boolean(plannerId),
    });
