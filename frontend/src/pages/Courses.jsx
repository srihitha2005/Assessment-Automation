import "./styles/CurriculumPages.css";

import { useLocation, useNavigate, useParams } from "react-router-dom";
import { CircularProgress } from "@mui/material";

import CourseCard from "../components/Curriculum_Components/CourseCard.jsx";
import CurriculumBreadcrumb from "../components/Curriculum_Components/CurriculumBreadcrumb.jsx";
import useCourses from "../hooks/Curriculum_Hooks/useCourses.js";

function Courses() {
    const navigate = useNavigate();
    const location = useLocation();
    const { gradeId } = useParams();

    const gradeName = location.state?.gradeName || `Grade ${gradeId}`;
    const { courses, loading, error } = useCourses(gradeId);

    const handleOpenCourse = (course) => {
        console.log("[Courses] Navigating to units for course:", course.courseId);
        navigate(`/grades/${gradeId}/courses/${course.courseId}/units`, {
            state: {
                gradeName,
                courseName: course.courseName
            }
        });
    };

    return (
        <div className="page-shell">
            <CurriculumBreadcrumb
                items={[
                    { label: "Curriculum", to: "/" },
                    { label: gradeName }
                ]}
            />

            <div className="page-header">
                <h1>{gradeName}</h1>
                <p>Select a course to continue.</p>
            </div>

            {
                loading ?
                    (
                        <div className="page-message">
                            <CircularProgress size={28} sx={{ mr: 1.5 }} />
                            Loading courses...
                        </div>
                    )
                    : error ?
                        (
                            <div className="page-error">
                                {error}
                            </div>
                        )
                        : courses.length === 0 ?
                            (
                                <div className="page-message">
                                    No courses found for this grade.
                                </div>
                            )
                            : (
                                <div className="curriculum-grid">
                                    {
                                        courses.map((course) => (
                                            <CourseCard
                                                key={course.courseId}
                                                course={course}
                                                onOpen={handleOpenCourse}
                                            />
                                        ))
                                    }
                                </div>
                            )
            }
        </div>
    );
}

export default Courses;
