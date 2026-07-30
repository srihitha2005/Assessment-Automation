# constants.py

SUCCESS = "SUCCESS"
FAILED = "FAILED"

DEFAULT_GENERATED_BY = "SYSTEM"

QUESTION_BANK_ROOT = "Question Bank"

OLLAMA_CLASSIFICATION_PROMPT = "classify_prompt.txt"
OLLAMA_GENERATION_PROMPT = "generate_prompt.txt"

MAX_GENERATION_RETRIES = 3

ASSESSMENT_STATUS_GENERATED = "Generated"
ASSESSMENT_STATUS_PARSED = "Parsed"
ASSESSMENT_STATUS_PUBLISHED = "Published"
ASSESSMENT_STATUS_NOT_GENERATED = "Not Generated"

QUESTION_TYPES = [
    "MCQ",
    "Short Answer",
    "Long Answer",
    "True / False",
    "Fill in the Blank",
]

DIFFICULTY_RATIOS = {
    "1-2": {"Easy": 0.40, "Medium": 0.50, "Hard": 0.10},
    "3-5": {"Easy": 0.30, "Medium": 0.60, "Hard": 0.10},
    "6-8": {"Easy": 0.20, "Medium": 0.60, "Hard": 0.20},
    "9-10": {"Easy": 0.15, "Medium": 0.60, "Hard": 0.25},
}

BLOOM_MARKS = {
    "Remember": 1,
    "Understand": 1,
    "Apply": 2,
    "Analyze": 2,
    "Evaluate": 3,
    "Create": 3,
}
