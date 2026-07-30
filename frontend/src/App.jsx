import { Route, Routes } from "react-router-dom";

import AppShell from "./AppShell.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import CurriculumBrowser from "./pages/CurriculumBrowser.jsx";
import PlannerBrowser from "./pages/PlannerBrowser.jsx";
import PlannerDetail from "./pages/PlannerDetail.jsx";
import AssessmentList from "./pages/AssessmentList.jsx";
import AssessmentEditor from "./pages/AssessmentEditor.jsx";
import VersionHistory from "./pages/VersionHistory.jsx";
import PublishFlow from "./pages/PublishFlow.jsx";
import QuestionBankBrowser from "./pages/QuestionBankBrowser.jsx";
import PropagationEvents from "./pages/PropagationEvents.jsx";
import NotFound from "./pages/NotFound.jsx";

const App = () => (
    <Routes>
        <Route element={<AppShell />}>
            <Route index element={<Dashboard />} />
            <Route path="curriculum" element={<CurriculumBrowser />} />
            <Route path="planners" element={<PlannerBrowser />} />
            <Route path="planners/:plannerId" element={<PlannerDetail />} />
            <Route path="assessments" element={<AssessmentList />} />
            <Route path="assessments/:assessmentId" element={<AssessmentEditor />} />
            <Route path="assessments/:assessmentId/versions" element={<VersionHistory />} />
            <Route path="assessments/:assessmentId/publish" element={<PublishFlow />} />
            <Route path="question-bank" element={<QuestionBankBrowser />} />
            <Route path="propagation" element={<PropagationEvents />} />
            <Route path="*" element={<NotFound />} />
        </Route>
    </Routes>
);

export default App;
