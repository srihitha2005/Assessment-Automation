import "./styles/CurriculumCard.css";
import Button from "../Commons/Button.jsx";

function GradeCard({ grade, onOpen }) {
    const handleOpen = () => {
        console.log("[GradeCard] Open grade clicked:", grade.gradeId, grade.gradeName);
        onOpen(grade);
    };

    return (
        <div className="curriculum-card">
            <div className="curriculum-card-header">
                <div>
                    <h2>{grade.gradeName}</h2>
                    <p>Browse courses available in this grade.</p>
                </div>
            </div>

            <div className="curriculum-card-details">
                <div>
                    <strong>Grade ID</strong>
                    <br />
                    {grade.gradeId}
                </div>
                <div>
                    <strong>Units</strong>
                    <br />
                    {grade.numberOfUnits ?? "--"}
                </div>
            </div>

            <div className="curriculum-card-footer">
                <Button text="View Courses" onClick={handleOpen} />
            </div>
        </div>
    );
}

export default GradeCard;
