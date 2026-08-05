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

export const useUnits = (gradeId, courseId) =>
    useQuery({
        queryKey: ["curriculum", "courses", gradeId, courseId, "units"],
        queryFn: () => curriculumApi.unitsByCourse(gradeId, courseId),
        enabled: Boolean(courseId) && Boolean(gradeId),
    });

export const useChapters = (gradeId, courseId, unitId) =>
    useQuery({
        queryKey: ["curriculum", "units", gradeId, courseId, unitId, "chapters"],
        queryFn: () => curriculumApi.chaptersByUnit(gradeId, courseId, unitId),
        enabled: Boolean(unitId) && Boolean(courseId) && Boolean(gradeId),
    });

export const usePlanners = () =>
    useQuery({ queryKey: ["planners"], queryFn: plannerApi.all });

export const usePlanner = (plannerId) =>
    useQuery({
        queryKey: ["planners", plannerId],
        queryFn: () => plannerApi.byId(plannerId),
        enabled: Boolean(plannerId),
    });

export const usePlannerDocument = (plannerId) =>
    useQuery({
        queryKey: ["planners", plannerId, "document"],
        queryFn: () => plannerApi.document(plannerId),
        enabled: false,
        retry: 1,
    });
