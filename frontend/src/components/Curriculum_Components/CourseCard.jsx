import "./styles/CurriculumCard.css";
import Button from "../Commons/Button.jsx";

function CourseCard({ course, onOpen }) {
    const handleOpen = () => {
        console.log("[CourseCard] Open course clicked:", course.courseId, course.courseName);
        onOpen(course);
    };

    return (
        <div className="curriculum-card">
            <div className="curriculum-card-header">
                <div>
                    <h2>{course.courseName}</h2>
                    <p>Browse units in this course.</p>
                </div>
            </div>

            <div className="curriculum-card-details">
                <div>
                    <strong>Course ID</strong>
                    <br />
                    {course.courseId}
                </div>
                <div>
                    <strong>Units</strong>
                    <br />
                    {course.numberOfUnits ?? "--"}
                </div>
            </div>

            <div className="curriculum-card-footer">
                <Button text="View Units" onClick={handleOpen} />
            </div>
        </div>
    );
}

export default CourseCard;
