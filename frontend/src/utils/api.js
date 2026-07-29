const delay = (ms = 1000) =>
    new Promise(resolve => setTimeout(resolve,ms));

const notImplemented = async (apiName) => {
    await delay();
    console.warn(`${apiName} is not connected to backend yet.`);

    return {
        success : false,
        message : `${apiName} is not implemented yet.`,
        data : null
    };
};

const dummy_getAllAssessments = async (apiName) => {
    await delay();

    return {
        success: true,
        message: `${apiName} Assessments dummy data`,
        data: [

            {
                assessmentId: 1001,
                assessmentNumber: 1,
                chapterName: "Nutrition in Plants",
                learningOutcomes: [
                    "Explain photosynthesis",
                    "Identify chlorophyll",
                    "Describe stomata",
                    "Understand autotrophic nutrition",
                    "Differentiate producers and consumers"
                ],
                learningOutcomeCount: 5,
                questionCount: 10,
                marks: 50,
                version: 4,
                status: "Generated"
            },

            {
                assessmentId: 1002,
                assessmentNumber: 2,
                chapterName: "Nutrition in Plants",
                learningOutcomes: [
                    "Explain aerobic respiration",
                    "Differentiate aerobic and anaerobic respiration",
                    "Identify products of respiration"
                ],
                learningOutcomeCount: 3,
                questionCount: 8,
                marks: 40,
                version: 2,
                status: "Published"
            },

            {
                assessmentId: 1003,
                assessmentNumber: 1,
                chapterName: "Transportation in Animals",
                learningOutcomes: [],
                learningOutcomeCount: 0,
                questionCount: 0,
                marks: 50,
                version: null,
                status: "Not Generated"
            },

            {
                assessmentId: 1004,
                assessmentNumber: 1,
                chapterName: "Human Digestive System",
                learningOutcomes: [
                    "Identify digestive organs",
                    "Explain digestion"
                ],
                learningOutcomeCount: 2,
                questionCount: 7,
                marks: 30,
                version: 1,
                status: "Parsed"
            },

            {
                assessmentId: 1005,
                assessmentNumber: 1,
                chapterName: "Reproduction in Plants",
                learningOutcomes: [],
                learningOutcomeCount: 0,
                questionCount: 0,
                marks: 50,
                version: null,
                status: "Not Generated"
            }

        ]
    };
};

const dummyAssessments = [
    {
        assessmentId: 1001,
        assessmentNumber: 1,
        chapterName: "Nutrition in Plants",
        learningOutcomes: [
            "Explain photosynthesis",
            "Identify chlorophyll",
            "Describe stomata",
            "Understand autotrophic nutrition",
            "Differentiate producers and consumers"
        ],
        learningOutcomeCount: 5,
        questionCount: 10,
        marks: 50,
        version: 4,
        status: "Generated",
        generatedOn: "28 Jul 2026 05:42 PM",
        generatedBy: "Joseph Stalin",
        updatedOn: "27 aug 2023 03:11 AM",
        updatedBy: "Joey Tribiani"
    },

    {
        assessmentId: 1002,
        assessmentNumber: 2,
        chapterName: "Nutrition in Plants",
        learningOutcomes: [
            "Explain aerobic respiration",
            "Differentiate aerobic and anaerobic respiration",
            "Identify products of respiration"
        ],
        learningOutcomeCount: 3,
        questionCount: 8,
        marks: 40,
        version: 2,
        status: "Published",
        generatedOn: "28 Jul 2026 05:42 PM",
        generatedBy: "Joseph Stalin",
        updatedOn: "27 aug 2023 03:11 AM",
        updatedBy: "Joey Tribiani"
    },

    {
        assessmentId: 1003,
        assessmentNumber: 1,
        chapterName: "Transportation in Animals",
        learningOutcomes: [],
        learningOutcomeCount: 0,
        questionCount: 0,
        marks: 50,
        version: null,
        status: "Not Generated",
        generatedOn: null,
        generatedBy: null,
        updatedOn: null,
        updatedBy: null

    },

    {
        assessmentId: 1004,
        assessmentNumber: 1,
        chapterName: "Human Digestive System",
        learningOutcomes: [
            "Identify digestive organs",
            "Explain digestion"
        ],
        learningOutcomeCount: 2,
        questionCount: 7,
        marks: 30,
        version: 1,
        status: "Parsed",
        generatedOn: "28 Jul 2026 05:42 PM",
        generatedBy: "Joseph Stalin",
        updatedOn: "27 aug 2023 03:11 AM",
        updatedBy: "Joey Tribiani"
    },

    {
        assessmentId: 1005,
        assessmentNumber: 1,
        chapterName: "Reproduction in Plants",
        learningOutcomes: [],
        learningOutcomeCount: 0,
        questionCount: 0,
        marks: 50,
        version: null,
        status: "Not Generated",
        generatedOn: null,
        generatedBy: null,
        updatedOn: null,
        updatedBy: null
    }
];
const dummyQuestions = {

    1001: [

        {
            questionId: 101,
            assessmentId: 1001,
            questionNumber: 1,
            version: 4,

            questionType: "MCQ",
            difficulty: "Easy",
            bloomsLevel: "Remember",

            learningOutcomeIds: [1, 2],

            marks: 2,

            images: [],

            question:
                "Which pigment is primarily responsible for photosynthesis?",

            options: [
                "Chlorophyll",
                "Melanin",
                "Keratin",
                "Haemoglobin"
            ],

            answer: "Chlorophyll",

            lastModifiedAt: "2026-07-28T10:15:00",
            lastModifiedBy: "John Doe"
        },

        {
            questionId: 102,
            assessmentId: 1001,
            questionNumber: 2,
            version: 4,

            questionType: "Short Answer",
            difficulty: "Medium",
            bloomsLevel: "Understand",

            learningOutcomeIds: [1, 3],

            marks: 3,

            images: [],

            question:
                "Explain how stomata help in photosynthesis.",

            options: [],

            answer:
                "Stomata enable gaseous exchange required for photosynthesis.",


            lastModifiedAt: "2026-07-28T10:15:00",
            lastModifiedBy: "John Doe"
        },

        {
            questionId: 103,
            assessmentId: 1001,
            questionNumber: 3,
            version: 4,

            questionType: "Long Answer",
            difficulty: "Hard",
            bloomsLevel: "Analyze",

            learningOutcomeIds: [1, 2, 3, 4, 5],

            marks: 5,

            images: [],

            question:
                "Explain the complete process of photosynthesis with a neat labelled diagram.",

            options: [],

            answer:
                "Photosynthesis is the process by which green plants prepare food using sunlight, carbon dioxide, water, and chlorophyll. Stomata facilitate gaseous exchange required for this process.",

            lastModifiedAt: "2026-07-30T14:20:00",
            lastModifiedBy: "John Doe"
        }

    ],

    1002: [

        {
            questionId: 201,
            assessmentId: 1002,
            questionNumber: 1,
            version: 2,

            questionType: "MCQ",
            difficulty: "Medium",
            bloomsLevel: "Apply",

            learningOutcomeIds: [1],

            marks: 2,

            images: [],

            question:
                "Which gas is required for aerobic respiration?",

            options: [
                "Oxygen",
                "Hydrogen",
                "Nitrogen",
                "Carbon Dioxide"
            ],

            answer: "Oxygen",

            lastModifiedAt: "2026-07-27T16:30:00",
            lastModifiedBy: "John Doe"
        },

        {
            questionId: 202,
            assessmentId: 1002,
            questionNumber: 2,
            version: 2,

            questionType: "True / False",
            difficulty: "Easy",
            bloomsLevel: "Remember",

            learningOutcomeIds: [2, 3],

            marks: 1,

            images: [],

            question:
                "Anaerobic respiration requires oxygen.",

            options: [
                "True",
                "False"
            ],

            answer: "False",

            lastModifiedAt: "2026-07-28T11:05:00",
            lastModifiedBy: "John Doe"
        }

    ],

    1003: [],

    1004: [

        {
            questionId: 401,
            assessmentId: 1004,
            questionNumber: 1,
            version: 1,

            questionType: "Diagram Based",
            difficulty: "Medium",
            bloomsLevel: "Understand",

            learningOutcomeIds: [1],

            marks: 5,

            images: [
                {
                    imageId: 1,
                    imageName: "digestive_system.png",
                    imagePath: "/images/digestive_system.png"
                }
            ],

            question:
                "Identify the labelled organs in the digestive system shown below.",

            options: [],

            answer:
                "Stomach, Liver, Pancreas, Small Intestine, Large Intestine.",

            lastModifiedAt: "2026-07-29T15:50:00",
            lastModifiedBy: "John Doe"
        },

        {
            questionId: 402,
            assessmentId: 1004,
            questionNumber: 2,
            version: 1,

            questionType: "Fill in the Blank",
            difficulty: "Easy",
            bloomsLevel: "Remember",

            learningOutcomeIds: [2],

            marks: 2,

            images: [],

            question:
                "The __________ is the largest gland in the human body.",

            options: [],

            answer: "Liver",

            lastModifiedAt: "2026-07-30T08:25:00",
            lastModifiedBy: "John Doe"
        }

    ],

    1005: []

};

const dummy_getQuestionsByAssessment = async (
    apiName,
    assessmentId
) => {

    console.log("[API] Fetching questions for assessment:", assessmentId);
    await delay();

    const questions = dummyQuestions[assessmentId] ?? [];
    console.log("[API] Questions found:", questions.length);

    return {

        success: true,

        message: `${apiName} Questions dummy data`,

        data: questions

    };

};

const dummy_getQuestionById = async (
    apiName,
    questionId
) => {

    await delay();

    const questions = Object.values(dummyQuestions).flat();

    const question = questions.find(
        question => question.questionId === questionId
    );

    if (!question) {

        return {

            success: false,

            message: "Question not found.",

            data: null

        };

    }

    return {

        success: true,

        message: `${apiName} Question dummy data`,

        data: question

    };

};

const dummy_generateDocument = async (apiName, assessmentId) => {

    await delay();

    return {

        success: true,

        message: `${apiName} Document generated successfully.`,

        data: {

            assessmentId,

            documentName: `Assessment_${assessmentId}.docx`,

            documentStatus: "Generated"

        }

    };

};

const dummy_getAssessmentsByID = async (apiName, assessmentId) => {
    console.log("[API] Fetching assessment ID:", assessmentId);
    await delay();
    const assessment = dummyAssessments.find(
        (assessment) => assessment.assessmentId === Number(assessmentId)
    );

    if (!assessment) {

        console.error("[API] Assessment not found:", assessmentId);

        return {
            success: false,
            message: "Assessment not found.",
            data: null
        };

    }

    console.log("[API] Assessment found:", assessment.assessmentId);

    return {
        success: true,
        message: `${apiName} Assessment dummy data`,
        data: assessment
    };

};
const api = {
    // Assessment APIs : all start with the normal local host / port/ assessments

    //should return Learning outcomes, marks of each assessment, version of assessment if id is there else return not there ( so can mark generated or not ) ,
    getAssessmentsByID: (assessmentId) => dummy_getAssessmentsByID("GET /id", assessmentId),
    //should return All assessments, their Chapters and AssesmentIds learning outcomes, marks, version.
    getAllAssessments: () => dummy_getAllAssessments("GET /all"),
    // should generate assesmnet and show success or failure
    generateAssesment: () => notImplemented("POST /generate"),
    //should regenerate assesment and show success or failure
    reGenerateAssesment: () => notImplemented("PUT /re-generate"),
    //should update adn show success or failure
    updateAssesment: () => notImplemented("PUT /update"),
    //should delete and show success or failure
    deleteAssessment: () => notImplemented("DELETE /delete"),
    //should publish an assesment and return success or failure
    publishAssessment: () => notImplemented("POST /publish"),
    //should paerse assignment and return success or failure
    parseAssesment: () => notImplemented("POST /parse"),

    // Question APIs : all start with the normal local host / port/ questions

    //should give  all questions and for each question should give question ,image if it is  there,  version, marks, id, type, answer, difficulty, blooms bucket, Learning outcome tested
    getQuestionsByAssessment: (assessmentID) => dummy_getQuestionsByAssessment("GET /assessment_id", assessmentID),
    //should give question , marks, type, answer, difficulty, version,  blooms bucket, image if  it is there, Learning outcomes tested
    getQuestionByID: (questionID) => dummy_getQuestionById("GET /id", questionID),
    //regenerate question , answer,  options if  they are there with or without prommmpt and return success or failure
    regenerateQuestion: () => notImplemented("POST /regenerate"),
    //update question or answer or options if they are there  by manual entry
    updateQuestion: () => notImplemented("PUT /update"),
    //add Question by ai with or without prompt / manually
    addQuestion: () => notImplemented("POST /add"),
    //delete question
    deleteQuestion: () => notImplemented("DELETE /delete"),
    regenerateAnswer: () => notImplemented("POST /regenerate-answer"),
    //Document APIs: all start with the normal local host / port/ document

    //should upload images
    uploadImage: () => notImplemented("POST /upload"),
    parseImage: () => notImplemented("POST /parse-images"),
    generateDocument: (assessmentID) => dummy_generateDocument("POST /generate-document", assessmentID),

    //version APIs : : all start with the normal local host / port/ versions
    rollbackQuestion: () => notImplemented("POST /question"),
    rollBackAssesment: () => notImplemented("POST /assessmnet")

};

export default api;
