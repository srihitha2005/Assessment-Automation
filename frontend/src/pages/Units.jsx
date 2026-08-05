import "./styles/CurriculumPages.css";

import { useLocation, useNavigate, useParams } from "react-router-dom";
import { CircularProgress } from "@mui/material";

import UnitCard from "../components/Curriculum_Components/UnitCard.jsx";
import CurriculumBreadcrumb from "../components/Curriculum_Components/CurriculumBreadcrumb.jsx";
import useUnits from "../hooks/Curriculum_Hooks/useUnits.js";

function Units() {
    const navigate = useNavigate();
    const location = useLocation();
    const { gradeId, courseId } = useParams();

    const gradeName = location.state?.gradeName || `Grade ${gradeId}`;
    const courseName = location.state?.courseName || `Course ${courseId}`;
    const { units, loading, error } = useUnits(gradeId, courseId);

    const handleOpenUnit = (unit) => {
        console.log("[Units] Navigating to chapters for unit:", unit.unitId);
        navigate(`/grades/${gradeId}/courses/${courseId}/units/${unit.unitId}/chapters`, {
            state: {
                gradeName,
                courseName,
                unitName: unit.unitName
            }
        });
    };

    return (
        <div className="page-shell">
            <CurriculumBreadcrumb
                items={[
                    { label: "Curriculum", to: "/" },
                    { label: gradeName, to: `/grades/${gradeId}/courses` },
                    { label: courseName }
                ]}
            />

            <div className="page-header">
                <h1>{courseName}</h1>
                <p>Select a unit to continue.</p>
            </div>

            {
                loading ?
                    (
                        <div className="page-message">
                            <CircularProgress size={28} sx={{ mr: 1.5 }} />
                            Loading units...
                        </div>
                    )
                    : error ?
                        (
                            <div className="page-error">
                                {error}
                            </div>
                        )
                        : units.length === 0 ?
                            (
                                <div className="page-message">
                                    No units found for this course.
                                </div>
                            )
                            : (
                                <div className="curriculum-grid">
                                    {
                                        units.map((unit) => (
                                            <UnitCard
                                                key={unit.unitId}
                                                unit={unit}
                                                onOpen={handleOpenUnit}
                                            />
                                        ))
                                    }
                                </div>
                            )
            }
        </div>
    );
}

export default Units;
