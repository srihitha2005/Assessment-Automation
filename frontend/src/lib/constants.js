export const STATUS_TOKENS = {
    Generated: { label: "Generated", color: "info" },
    Parsed: { label: "Parsed", color: "warning" },
    Published: { label: "Published", color: "success" },
    Outdated: { label: "Outdated", color: "danger" },
    "Not Generated": { label: "Not Generated", color: "neutral" },
};

export const DIFFICULTY_TOKENS = {
    Easy: "success",
    Medium: "warning",
    Hard: "danger",
};

export const BLOOM_LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"];

export const QUESTION_TYPES = ["MCQ", "Short Answer", "Long Answer", "True / False", "Fill in the Blank"];

export const NAV_ITEMS = [
    { to: "/", label: "Dashboard", icon: "◉" },
    { to: "/curriculum", label: "Curriculum", icon: "▤" },
    { to: "/planners", label: "Planners", icon: "▦" },
    { to: "/assessments", label: "Assessments", icon: "❑" },
    { to: "/question-bank", label: "Question Bank", icon: "?" },
    { to: "/propagation", label: "Propagation", icon: "↻" },
];
