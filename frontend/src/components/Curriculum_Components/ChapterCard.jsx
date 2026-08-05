import "./styles/CurriculumCard.css";
import Button from "../Commons/Button.jsx";

function ChapterCard({ chapter }) {
    return (
        <div className="curriculum-card">
            <div className="curriculum-card-header">
                <div>
                    <h2>{chapter.chapterName}</h2>
                </div>
            </div>
        </div>
    );
}

export default ChapterCard;
