import "./styles/CurriculumPages.css";

import { useLocation, useNavigate, useParams } from "react-router-dom";
import { CircularProgress } from "@mui/material";

import ChapterCard from "../components/Curriculum_Components/ChapterCard.jsx";
import CurriculumBreadcrumb from "../components/Curriculum_Components/CurriculumBreadcrumb.jsx";
import useChapters from "../hooks/Curriculum_Hooks/useChapters.js";

function Chapters() {
    const navigate = useNavigate();
    const location = useLocation();
    const { gradeId, courseId, unitId } = useParams();

    const gradeName = location.state?.gradeName || `Grade ${gradeId}`;
    const courseName = location.state?.courseName || `Course ${courseId}`;
    const unitName = location.state?.unitName || `Unit ${unitId}`;
    const { chapters, loading, error } = useChapters(gradeId, courseId, unitId);

    return (
        <div className="page-shell">
            <CurriculumBreadcrumb
                items={[
                    { label: "Curriculum", to: "/" },
                    { label: gradeName, to: `/grades/${gradeId}/courses` },
                    {
                        label: courseName,
                        to: `/grades/${gradeId}/courses/${courseId}/units`
                    },
                    { label: unitName }
                ]}
            />

            <div className="page-header">
                <h1>{unitName}</h1>
                <p>Select a chapter to view assessments.</p>
            </div>

            {
                loading ?
                    (
                        <div className="page-message">
                            <CircularProgress size={28} sx={{ mr: 1.5 }} />
                            Loading chapters...
                        </div>
                    )
                    : error ?
                        (
                            <div className="page-error">
                                {error}
                            </div>
                        )
                        : chapters.length === 0 ?
                            (
                                <div className="page-message">
                                    No chapters found for this unit.
                                </div>
                            )
                            : (
                                <div className="curriculum-grid">
                                    {
                                        chapters.map((chapter) => (
                                            <ChapterCard
                                                key={chapter.chapterId}
                                                chapter={chapter}
                                            />
                                        ))
                                    }
                                </div>
                            )
            }
        </div>
    );
}

export default Chapters;
