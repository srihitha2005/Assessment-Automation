import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { questionApi } from "../lib/api.js";

const invalidate = (qc, assessmentId) => {
    qc.invalidateQueries({ queryKey: ["assessments"] });
    if (assessmentId) {
        qc.invalidateQueries({ queryKey: ["assessments", assessmentId] });
        qc.invalidateQueries({ queryKey: ["assessments", assessmentId, "questions"] });
        qc.invalidateQueries({ queryKey: ["assessments", assessmentId, "versions"] });
    }
    qc.invalidateQueries({ queryKey: ["dashboard"] });
};

export const useUpdateQuestion = (assessmentId) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: ({ questionId, payload }) => questionApi.update(questionId, payload),
        onSuccess: () => {
            invalidate(qc, assessmentId);
            toast.success("Question updated.");
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useDeleteQuestion = (assessmentId) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: (questionId) => questionApi.remove(questionId),
        onSuccess: () => {
            invalidate(qc, assessmentId);
            toast.success("Question deleted.");
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useRegenerateQuestion = (assessmentId) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: ({ questionId, prompt }) =>
            questionApi.regenerate(questionId, { prompt }),
        onSuccess: () => {
            invalidate(qc, assessmentId);
            toast.success("Question regenerated.");
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useRegenerateAnswer = (assessmentId) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: ({ questionId, prompt }) =>
            questionApi.regenerateAnswer(questionId, { prompt }),
        onSuccess: () => {
            invalidate(qc, assessmentId);
            toast.success("Answer regenerated.");
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useUploadImages = (assessmentId) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: ({ questionId, files }) => {
            const form = new FormData();
            for (const file of files) form.append("files", file);
            return questionApi.uploadImages(questionId, form);
        },
        onSuccess: (data) => {
            invalidate(qc, assessmentId);
            toast.success(`Uploaded ${data?.length ?? 0} image(s).`);
        },
        onError: (error) => toast.error(error.message),
    });
};

export const useDeleteImage = (assessmentId) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: (imageId) => questionApi.deleteImage(imageId),
        onSuccess: () => {
            invalidate(qc, assessmentId);
            toast.success("Image deleted.");
        },
        onError: (error) => toast.error(error.message),
    });
};
