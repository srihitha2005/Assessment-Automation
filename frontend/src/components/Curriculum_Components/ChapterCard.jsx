import "./styles/CurriculumCard.css";
import Button from "../Commons/Button.jsx";

function ChapterCard({ chapter, onOpen }) {
    const handleOpen = () => {
        console.log("[ChapterCard] Open chapter clicked:", chapter.chapterId, chapter.chapterName);
        onOpen(chapter);
    };

    return (
        <div className="curriculum-card">
            <div className="curriculum-card-header">
                <div>
                    <h2>{chapter.chapterName}</h2>
                    <p>View and generate assessments for this chapter.</p>
                </div>
            </div>

            <div className="curriculum-card-details">
                <div>
                    <strong>Chapter ID</strong>
                    <br />
                    {chapter.chapterId}
                </div>
                <div>
                    <strong>Assessments</strong>
                    <br />
                    {chapter.numberOfAssessments ?? "--"}
                </div>
            </div>

            <div className="curriculum-card-footer">
                <Button text="View Assessments" onClick={handleOpen} />
            </div>
        </div>
    );
}

export default ChapterCard;
