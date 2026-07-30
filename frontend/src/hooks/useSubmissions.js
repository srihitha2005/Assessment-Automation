import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { submissionApi } from "../lib/api.js";

export const useSubmissions = (assessmentId) =>
    useQuery({
        queryKey: ["assessments", assessmentId, "submissions"],
        queryFn: () => submissionApi.forAssessment(assessmentId),
        enabled: Boolean(assessmentId),
    });

export const useCreateSubmission = (assessmentId) => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: (payload) => submissionApi.create(assessmentId, payload),
        onSuccess: (data) => {
            qc.invalidateQueries({ queryKey: ["assessments", assessmentId, "submissions"] });
            qc.invalidateQueries({ queryKey: ["dashboard"] });
            toast.success(`Submission recorded (score ${data.score}/${data.maxScore}).`);
        },
        onError: (error) => toast.error(error.message),
    });
};
