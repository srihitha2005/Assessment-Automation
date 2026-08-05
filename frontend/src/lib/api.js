import { http, get, post, put, del } from "./http.js";

export const curriculumApi = {
    grades: () => get("/grades"),
    coursesByGrade: (gradeId) => get(`/grades/${gradeId}/courses`),
    unitsByCourse: (gradeId, courseId) => get(`/courses/${gradeId}/${courseId}/units`),
    chaptersByUnit: (gradeId, courseId, unitId) => get(`/units/${gradeId}/${courseId}/${unitId}/chapters`),
    resolve: (payload) => post("/curriculum", payload),
    assessmentsForCurriculum: (curriculumId) => get(`/curriculum/${curriculumId}/assessments`),
};

export const plannerApi = {
    all: () => get("/planners"),
    byId: (plannerId) => get(`/planners/${plannerId}`),
    updateOutcomes: (plannerId, payload) => post(`/planners/${plannerId}/outcomes`, payload),
};

export const assessmentApi = {
    all: () => get("/assessments"),
    byId: (id) => get(`/assessments/${id}`),
    questions: (id) => get(`/assessments/${id}/questions`),
    versions: (id) => get(`/assessments/${id}/versions`),
    generate: (payload) => post("/assessments", payload),
    regenerate: (id, payload) => post(`/assessments/${id}/regenerate`, payload),
    remove: (id) => del(`/assessments/${id}`),
    parse: (id) => post(`/assessments/${id}/parse`),
    publish: (id, payload = {}) => post(`/assessments/${id}/publish`, payload),
    rollback: (id, payload) => post(`/assessments/${id}/rollback`, payload),
    docxUrl: (id) => `${http.defaults.baseURL}/assessments/${id}/docx`,
    pdfUrl: (id) => `${http.defaults.baseURL}/assessments/${id}/pdf`,
    addQuestion: (id, payload) => post(`/assessments/${id}/questions`, payload),
};

export const questionApi = {
    byId: (id) => get(`/questions/${id}`),
    update: (id, payload) => put(`/questions/${id}`, payload),
    remove: (id) => del(`/questions/${id}`),
    regenerate: (id, payload) => post(`/questions/${id}/regenerate`, payload),
    regenerateAnswer: (id, payload) => post(`/questions/${id}/answer/regenerate`, payload),
    uploadImages: (id, formData) =>
        http
            .post(`/questions/${id}/images`, formData, {
                headers: { "Content-Type": "multipart/form-data" },
            })
            .then((response) => response.data?.data ?? response.data),
    deleteImage: (imageId) => del(`/images/${imageId}`),
};

export const submissionApi = {
    forAssessment: (id) => get(`/assessments/${id}/submissions`),
    create: (id, payload) => post(`/assessments/${id}/submissions`, payload),
};

export const dashboardApi = {
    summary: () => get("/dashboard/summary"),
};

export const propagationApi = {
    events: () => get("/propagation/events"),
};
