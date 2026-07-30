import { useQuery } from "@tanstack/react-query";

import { dashboardApi } from "../lib/api.js";

export const useDashboardSummary = () =>
    useQuery({ queryKey: ["dashboard"], queryFn: dashboardApi.summary });
