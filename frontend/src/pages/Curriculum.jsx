import "./styles/CurriculumPages.css";

import { useNavigate } from "react-router-dom";
import { CircularProgress } from "@mui/material";

import GradeCard from "../components/Curriculum_Components/GradeCard.jsx";
import CurriculumBreadcrumb from "../components/Curriculum_Components/CurriculumBreadcrumb.jsx";
import useGrades from "../hooks/Curriculum_Hooks/useGrades.js";

function Curriculum() {
    const navigate = useNavigate();
    const { grades, loading, error } = useGrades();

    const handleOpenGrade = (grade) => {
        console.log("[Curriculum] Navigating to courses for grade:", grade.gradeId);
        navigate(`/grades/${grade.gradeId}/courses`, {
            state: { gradeName: grade.gradeName }
        });
    };

    return (
        <div className="page-shell">
            <CurriculumBreadcrumb
                items={[
                    { label: "Curriculum" }
                ]}
            />

            <div className="page-header">
                <h1>Curriculum</h1>
                <p>Select a grade to browse courses, units, chapters and assessments.</p>
            </div>

            {
                loading ?
                    (
                        <div className="page-message">
                            <CircularProgress size={28} sx={{ mr: 1.5 }} />
                            Loading grades...
                        </div>
                    )
                    : error ?
                        (
                            <div className="page-error">
                                {error}
                            </div>
                        )
                        : grades.length === 0 ?
                            (
                                <div className="page-message">
                                    No grades found.
                                </div>
                            )
                            : (
                                <div className="curriculum-grid">
                                    {
                                        grades.map((grade) => (
                                            <GradeCard
                                                key={grade.gradeId}
                                                grade={grade}
                                                onOpen={handleOpenGrade}
                                            />
                                        ))
                                    }
                                </div>
                            )
            }
        </div>
    );
}

export default Curriculum;
