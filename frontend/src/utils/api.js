import axios from "axios";

// Use relative URLs in development so Vite can proxy to the FastAPI backend.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

const client = axios.create({
    baseURL: BASE_URL,
    headers: {
        "Content-Type": "application/json"
    }
});

client.interceptors.request.use(
    (config) => {
        console.log("[API] Request:", config.method?.toUpperCase(), config.url, {
            params: config.params,
            data: config.data
        });
        return config;
    },
    (error) => {
        console.error("[API] Request error:", error);
        return Promise.reject(error);
    }
);

client.interceptors.response.use(
    (response) => {
        console.log("[API] Response:", response.config.url, response.data);
        return response;
    },
    (error) => {
        console.error("[API] Response error:", error?.response?.status, error?.response?.data || error.message);
        return Promise.reject(error);
    }
);

const wrapSuccess = (data, message = "Success") => ({
    success: true,
    message,
    data
});

const wrapError = (error, fallbackMessage) => {
    const message =
        error?.response?.data?.detail ||
        error?.response?.data?.message ||
        error?.message ||
        fallbackMessage;

    return {
        success: false,
        message,
        data: null
    };
};

const api = {

    // Curriculum APIs
    getAllGrades: async () => {
        try {
            console.log("[API] getAllGrades");
            const response = await client.get("/curriculum/grades");
            return wrapSuccess(response.data, "Grades fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch grades.");
        }
    },

    getCoursesByGrade: async (gradeId) => {
        try {
            console.log("[API] getCoursesByGrade:", gradeId);
            const response = await client.get(`/curriculum/grades/${gradeId}/courses`);
            return wrapSuccess(response.data, "Courses fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch courses.");
        }
    },

    getUnitsByCourse: async (gradeId, courseId) => {
        try {
            console.log("[API] getUnitsByCourse:", { gradeId, courseId });
            const response = await client.get(`/curriculum/courses/${gradeId}/${courseId}/units`);
            return wrapSuccess(response.data, "Units fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch units.");
        }
    },

    getChaptersByUnit: async (gradeId, courseId, unitId) => {
        try {
            console.log("[API] getChaptersByUnit:", { gradeId, courseId, unitId });
            const response = await client.get(`/curriculum/units/${gradeId}/${courseId}/${unitId}/chapters`);
            return wrapSuccess(response.data, "Chapters fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch chapters.");
        }
    },

    getCurriculumId: async (gradeId, courseId, unitId, chapterId) => {
        try {
            console.log("[API] getCurriculumId:", { gradeId, courseId, unitId, chapterId });
            const response = await client.post("/curriculum/id", null, {
                params: {
                    grade_id: gradeId,
                    course_id: courseId,
                    unit_id: unitId,
                    chapter_id: chapterId
                }
            });
            return wrapSuccess(response.data, "Curriculum ID fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch curriculum ID.");
        }
    },

    getAssessmentsByCurriculum: async (curriculumId) => {
        try {
            console.log("[API] getAssessmentsByCurriculum:", curriculumId);
            const response = await client.get(`/curriculum/${curriculumId}/assessments`);
            return wrapSuccess(response.data, "Assessments fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch assessments.");
        }
    },

    // Assessment APIs
    getAssessmentsByID: async (assessmentId) => {
        try {
            console.log("[API] getAssessmentsByID:", assessmentId);
            const response = await client.get(`/assessments/${assessmentId}/details`);
            return wrapSuccess(response.data, "Assessment details fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch assessment details.");
        }
    },

    getAllAssessments: async (curriculumId) => {
        try {
            console.log("[API] getAllAssessments for curriculum:", curriculumId);
            const response = await client.get(`/curriculum/${curriculumId}/assessments`);
            return wrapSuccess(response.data, "Assessments fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch assessments.");
        }
    },

    generateAssesment: async (curriculumId, prompt = "") => {
        try {
            console.log("[API] generateAssesment:", { curriculumId, prompt });
            const response = await client.post("/assessments", null, {
                params: {
                    curriculum_id: curriculumId,
                    prompt
                }
            });
            return wrapSuccess(response.data, response.data?.message || "Assessment generated successfully.");
        } catch (error) {
            return wrapError(error, "Unable to generate assessment.");
        }
    },

    reGenerateAssesment: async (assessmentId, prompt = "") => {
        try {
            console.log("[API] reGenerateAssesment:", { assessmentId, prompt });
            const response = await client.post(`/assessments/${assessmentId}/regenerate`, null, {
                params: { prompt }
            });
            return wrapSuccess(response.data, response.data?.message || "Assessment regenerated successfully.");
        } catch (error) {
            return wrapError(error, "Unable to regenerate assessment.");
        }
    },

    deleteAssessment: async (assessmentId) => {
        try {
            console.log("[API] deleteAssessment:", assessmentId);
            const response = await client.delete(`/assessments/${assessmentId}`);
            return wrapSuccess(response.data, response.data?.message || "Assessment deleted successfully.");
        } catch (error) {
            return wrapError(error, "Unable to delete assessment.");
        }
    },

    publishAssessment: async (assessmentId) => {
        try {
            console.log("[API] publishAssessment:", assessmentId);
            const response = await client.post(`/assessments/${assessmentId}/publish`);
            return wrapSuccess(response.data, response.data?.message || "Assessment published successfully.");
        } catch (error) {
            return wrapError(error, "Unable to publish assessment.");
        }
    },

    rollBackAssesment: async (assessmentId) => {
        try {
            console.log("[API] rollBackAssesment:", assessmentId);
            const response = await client.post(`/assessments/${assessmentId}/rollback`);
            return wrapSuccess(response.data, response.data?.message || "Assessment rolled back successfully.");
        } catch (error) {
            return wrapError(error, "Unable to rollback assessment.");
        }
    },

    generateDocument: async (assessmentId) => {
        try {
            console.log("[API] generateDocument:", assessmentId);
            const response = await client.get(`/assessments/${assessmentId}/docx`);
            return wrapSuccess(response.data, response.data?.message || "DOCX generated successfully.");
        } catch (error) {
            return wrapError(error, "Unable to generate document.");
        }
    },

    generateMoreQuestions: async (assessmentId) => {
        try {
            console.log("[API] generateMoreQuestions:", assessmentId);
            const response = await client.post(`/assessments/${assessmentId}/questions/generate`);
            return wrapSuccess(response.data, response.data?.message || "Additional questions generated successfully.");
        } catch (error) {
            return wrapError(error, "Unable to generate more questions.");
        }
    },

    // Question APIs
    getQuestionsByAssessment: async (assessmentId) => {
        try {
            console.log("[API] getQuestionsByAssessment:", assessmentId);
            const response = await client.get(`/assessments/${assessmentId}`);
            const questions = response.data?.questions || [];

            const detailedQuestions = await Promise.all(
                questions.map(async (item) => {
                    try {
                        const detailResponse = await client.get(`/questions/${item.questionId}`);
                        return {
                            ...item,
                            ...detailResponse.data,
                            images: detailResponse.data?.images || item.images || []
                        };
                    } catch (detailError) {
                        console.warn("[API] Falling back to list question data:", item.questionId, detailError);
                        return {
                            ...item,
                            images: item.images || [],
                            options: item.options || [],
                            questionType: item.questionType || "Short Answer",
                            difficulty: item.difficulty || "Medium",
                            bloomsLevel: item.bloomLevel || item.bloomsLevel || "-"
                        };
                    }
                })
            );

            return wrapSuccess(detailedQuestions, "Questions fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch questions.");
        }
    },

    getQuestionByID: async (questionId) => {
        try {
            console.log("[API] getQuestionByID:", questionId);
            const response = await client.get(`/questions/${questionId}`);
            const data = {
                ...response.data,
                images: response.data?.images || [],
                options: response.data?.options || [],
                bloomsLevel: response.data?.bloomLevel || response.data?.bloomsLevel
            };
            return wrapSuccess(data, "Question fetched successfully.");
        } catch (error) {
            return wrapError(error, "Unable to fetch question.");
        }
    },

    regenerateQuestion: async (questionId, prompt = "") => {
        try {
            console.log("[API] regenerateQuestion:", { questionId, prompt });
            const response = await client.post(`/questions/${questionId}/regenerate`, null, {
                params: { prompt }
            });
            return wrapSuccess(response.data, response.data?.message || "Question regenerated successfully.");
        } catch (error) {
            return wrapError(error, "Unable to regenerate question.");
        }
    },

    regenerateQuestionWithPrompt: async (questionId, prompt = "") => {
        return api.regenerateQuestion(questionId, prompt);
    },

    updateQuestion: async (questionId, question, answer) => {
        try {
            console.log("[API] updateQuestion:", { questionId, question, answer });
            const response = await client.put(`/questions/${questionId}`, null, {
                params: { question, answer }
            });
            return wrapSuccess(response.data, response.data?.message || "Question updated successfully.");
        } catch (error) {
            return wrapError(error, "Unable to update question.");
        }
    },

    deleteQuestion: async (questionId) => {
        try {
            console.log("[API] deleteQuestion:", questionId);
            const response = await client.delete(`/questions/${questionId}`);
            return wrapSuccess(response.data, response.data?.message || "Question deleted successfully.");
        } catch (error) {
            return wrapError(error, "Unable to delete question.");
        }
    },

    regenerateAnswer: async (questionId, prompt = "") => {
        try {
            console.log("[API] regenerateAnswer:", { questionId, prompt });
            const response = await client.post(`/questions/${questionId}/answer/regenerate`, null, {
                params: { prompt }
            });
            return wrapSuccess(response.data, response.data?.message || "Answer regenerated successfully.");
        } catch (error) {
            return wrapError(error, "Unable to regenerate answer.");
        }
    },

    rollbackQuestion: async (questionId) => {
        try {
            console.log("[API] rollbackQuestion:", questionId);
            const response = await client.post(`/questions/${questionId}/rollback`);
            return wrapSuccess(response.data, response.data?.message || "Question rolled back successfully.");
        } catch (error) {
            return wrapError(error, "Unable to rollback question.");
        }
    },

    uploadImage: async (questionId, images) => {
        try {
            console.log("[API] uploadImage:", questionId);
            const formData = new FormData();

            if (images) {
                const fileList = Array.isArray(images) ? images : [images];
                fileList.forEach((file) => {
                    formData.append("image[]", file);
                });
            }

            const response = await client.post(`/questions/${questionId}/images`, formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            return wrapSuccess(response.data, response.data?.message || "Image(s) uploaded successfully.");
        } catch (error) {
            return wrapError(error, "Unable to upload image(s).");
        }
    },

    deleteImage: async (imageId) => {
        try {
            console.log("[API] deleteImage:", imageId);
            const response = await client.delete(`/questions/images/${imageId}`);
            return wrapSuccess(response.data, response.data?.message || "Image deleted successfully.");
        } catch (error) {
            return wrapError(error, "Unable to delete image.");
        }
    },

    addQuestion: async (assessmentId) => {
        try {
            console.log("[API] addQuestion via generateMoreQuestions:", assessmentId);
            return await api.generateMoreQuestions(assessmentId);
        } catch (error) {
            return wrapError(error, "Unable to add question.");
        }
    },

    parseAssesment: async () => {
        console.warn("[API] parseAssesment is not available in the backend.");
        return {
            success: false,
            message: "Parse assessment is not available in the backend.",
            data: null
        };
    }

};

export default api;
