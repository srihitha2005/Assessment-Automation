import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { plannerApi, propagationApi } from "../lib/api.js";

export const usePropagationEvents = () =>
    useQuery({ queryKey: ["propagation"], queryFn: propagationApi.events });

export const useUpdatePlannerOutcomes = () => {
    const qc = useQueryClient();
    return useMutation({
        mutationFn: ({ plannerId, payload }) => plannerApi.updateOutcomes(plannerId, payload),
        onSuccess: (data) => {
            qc.invalidateQueries({ queryKey: ["propagation"] });
            qc.invalidateQueries({ queryKey: ["assessments"] });
            qc.invalidateQueries({ queryKey: ["planners"] });
            toast.success(
                `Propagation event recorded (${data.affectedAssessmentIds.length} assessment(s) impacted).`,
            );
        },
        onError: (error) => toast.error(error.message),
    });
};
