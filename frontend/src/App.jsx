import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

import Curriculum from "./pages/Curriculum.jsx";
import Courses from "./pages/Courses.jsx";
import Units from "./pages/Units.jsx";
import Chapters from "./pages/Chapters.jsx";
import AssessmentViewer from "./pages/AssessmentViewer.jsx";
import AssessmentEditor from "./pages/AssessmentEditor.jsx";

const theme = createTheme({
    palette: {
        primary: {
            main: "#2563EB"
        },
        background: {
            default: "#F4F7FB"
        },
        text: {
            primary: "#1E293B",
            secondary: "#64748B"
        }
    },
    typography: {
        fontFamily: "Arial, Helvetica, sans-serif"
    },
    shape: {
        borderRadius: 12
    }
});

function App() {
    console.log("[App] Rendering Assessment Automation frontend.");

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <BrowserRouter>
                <Routes>
                    <Route
                        path="/"
                        element={<Curriculum />}
                    />

                    <Route
                        path="/grades/:gradeId/courses"
                        element={<Courses />}
                    />

                    <Route
                        path="/grades/:gradeId/courses/:courseId/units"
                        element={<Units />}
                    />

                    <Route
                        path="/grades/:gradeId/courses/:courseId/units/:unitId/chapters"
                        element={<Chapters />}
                    />

                    <Route
                        path="/grades/:gradeId/courses/:courseId/units/:unitId/chapters/:chapterId/assessments"
                        element={<AssessmentViewer />}
                    />

                    <Route
                        path="/view-assessment/:assessmentId"
                        element={<AssessmentEditor />}
                    />

                    <Route
                        path="/view-assessments"
                        element={<Navigate to="/" replace />}
                    />

                    <Route
                        path="*"
                        element={<Navigate to="/" replace />}
                    />
                </Routes>
            </BrowserRouter>
        </ThemeProvider>
    );
}

export default App;
