import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "/api";

export const http = axios.create({
    baseURL,
    timeout: 120_000,
    headers: {
        "Content-Type": "application/json",
    },
});

http.interceptors.response.use(
    (response) => response,
    (error) => {
        const message =
            error.response?.data?.message ||
            error.response?.data?.detail ||
            error.message ||
            "Unknown error";
        return Promise.reject(new Error(message));
    },
);

const unwrap = (response) => response.data?.data ?? response.data;

export const get = (path, config) => http.get(path, config).then(unwrap);
export const post = (path, body, config) => http.post(path, body, config).then(unwrap);
export const put = (path, body, config) => http.put(path, body, config).then(unwrap);
export const del = (path, config) => http.delete(path, config).then(unwrap);
