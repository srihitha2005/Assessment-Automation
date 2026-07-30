import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { assessmentApi } from "../lib/api.js";

const KEY = ["assessments"];

export const useAssessments = () =>
    useQuery({ queryKey: KEY, queryFn: assessmentApi.all });

export const useAssessment = (id) =>
    useQuery({
        queryKey: [...KEY, id],
        queryFn: () => assessmentApi.byId(id),
        enabled: Boolean(id),
    });

export const useAssessmentQuestions = (id) =>
    useQuery({
        queryKey: [...KEY, id, "questions"],
        queryFn: () => assessmentApi.questions(id),
        enabled: Boolean(id),
    });

export const useAssessmentVersions = (id) =>
    useQuery({
        queryKey: [...KEY, id, "versions"],
        queryFn: () => assessmentApi.versions(id),
        enabled: Boolean(id),
    });

const invalidateAll = (qc, id) => {
    qc.invalidateQueries({ queryKey: KEY });
    if (id) {
        qc.invalidateQueries({ queryKey: [...KEY, id] });
        qc.invalidateQueries({ queryKey: [...KEY, id, "questions"] });
        qc.invalidateQueries({ queryKey: [...KEY, id, "versions"] });
    }
    qc.invalidateQueries({ queryKey: ["dashboard"] });
};

export const useGenerateAssessment = () => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: assessmentApi.generate,
        onSuccess: (data) => {
            invalidateAll(qc);
            toast.success("Assessment generated.");
            return data;
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useRegenerateAssessment = (id) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: (payload) => assessmentApi.regenerate(id, payload),
        onSuccess: () => {
            invalidateAll(qc, id);
            toast.success("Assessment regenerated.");
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useDeleteAssessment = () => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: (id) => assessmentApi.remove(id),
        onSuccess: () => {
            invalidateAll(qc);
            toast.success("Assessment deleted.");
        },
        onError: (error) => toast.error(error.message),
    });
};

export const usePublishAssessment = (id) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: (payload = {}) => assessmentApi.publish(id, payload),
        onSuccess: (data) => {
            invalidateAll(qc, id);
            toast.success(
                data?.receipt?.mode === "artifact"
                    ? "Published (demo artifact written to disk)."
                    : "Assessment published to portal.",
            );
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useParseAssessment = (id) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: () => assessmentApi.parse(id),
        onSuccess: (data) => {
            invalidateAll(qc, id);
            toast.success(`Parsed ${data?.questions?.length ?? 0} questions.`);
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useRollbackAssessment = (id) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: (payload) => assessmentApi.rollback(id, payload),
        onSuccess: () => {
            invalidateAll(qc, id);
            toast.success("Rolled back.");
        },
        onError: (error) => toast.error(error.message),
    });
};
