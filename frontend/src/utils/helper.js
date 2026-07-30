import {STATUS_COLORS} from "./constants.js";

export const getStatusColor = (status) => {
  return STATUS_COLORS[status] || "#9CA3AF";
};

export const formatVersion = (version) => {
    return version ? `v${version}` : "--";
};

export const getLearningOutcomeCount = (learningOutcomes) => {
    if (!learningOutcomes)
        return 0;
    return learningOutcomes.length;
};

export const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
        case "Easy":
            return "#16A34A";
        case "Medium":
            return "#F59E0B";
        case "Hard":
            return "#DC2626";
        default:
            return "#64748B";
    }
};

export const getQuestionTypeBadgeColor = (type) => {
    switch (type) {
        case "MCQ":
            return "#2563EB";
        case "Short Answer":
            return "#7C3AED";
        case "Long Answer":
            return "#EA580C";
        case "True / False":
            return "#0891B2";
        case "Fill in the Blank":
            return "#15803D";
        default:
            return "#64748B";
    }
};

export const hasImages = (question) => {
    return Array.isArray(question?.images) && question.images.length > 0;
};

export const normalizeLearningOutcomes = (learningOutcomes = []) => {
    return learningOutcomes.map((item, index) => {
        if (typeof item === "string") {
            return {
                learningOutcomeId: `LO${index + 1}`,
                description: item
            };
        }

        return {
            learningOutcomeId: item.learningOutcomeId || `LO${index + 1}`,
            description: item.description || item.learningOutcome || String(item)
        };
    });
};

export const getLearningOutcomeDescriptions = (
    learningOutcomeIds,
    learningOutcomes
) => {
    return learningOutcomes.filter((learningOutcome) =>
        learningOutcomeIds.includes(learningOutcome.learningOutcomeId)
    );
};
