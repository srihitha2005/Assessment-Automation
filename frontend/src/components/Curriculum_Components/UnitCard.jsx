import "./styles/CurriculumCard.css";
import Button from "../Commons/Button.jsx";

function UnitCard({ unit, onOpen }) {
    const handleOpen = () => {
        console.log("[UnitCard] Open unit clicked:", unit.unitId, unit.unitName);
        onOpen(unit);
    };

    return (
        <div className="curriculum-card">
            <div className="curriculum-card-header">
                <div>
                    <h2>{unit.unitName}</h2>
                    <p>Browse chapters in this unit.</p>
                </div>
            </div>

            <div className="curriculum-card-details">
                <div>
                    <strong>Unit ID</strong>
                    <br />
                    {unit.unitId}
                </div>
                <div>
                    <strong>Chapters</strong>
                    <br />
                    {unit.numberOfChapters ?? "--"}
                </div>
            </div>

            <div className="curriculum-card-footer">
                <Button text="View Chapters" onClick={handleOpen} />
            </div>
        </div>
    );
}

export default UnitCard;
