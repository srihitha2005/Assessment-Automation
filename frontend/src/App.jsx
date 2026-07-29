import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import AssessmentViewer from "./pages/AssessmentViewer.jsx";
import AssessmentEditor from "./pages/AssessmentEditor.jsx";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={
                        <Navigate
                            to="/view-assessments"
                            replace
                        />
                    }
                />

                <Route
                    path="/view-assessments"
                    element={<AssessmentViewer />}
                />

                <Route
                    path="/view-assessment/:assessmentId"
                    element={<AssessmentEditor />}
                />

            </Routes>

        </BrowserRouter>

    );

}

export default App;