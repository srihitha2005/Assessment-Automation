import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import { useChapters, useCourses, useGrades, useUnits } from "../hooks/useCurriculum.js";
import "./CurriculumBrowser.css";

const Column = ({ title, hint, items, active, onSelect, renderItem, isLoading }) => (
    <Card padding="none">
        <CardHeader>
            <div>
                <div className="col__title">{title}</div>
                {hint && <div className="col__hint">{hint}</div>}
            </div>
        </CardHeader>
        <CardBody className="col__body">
            {isLoading ? (
                <Spinner label="Loading…" />
            ) : items?.length ? (
                <ul className="col__list">
                    {items.map((item) => (
                        <li key={item.id}>
                            <button
                                className={`col__button ${item.id === active ? "col__button--active" : ""}`}
                                onClick={() => onSelect(item.id)}
                            >
                                {renderItem(item)}
                            </button>
                        </li>
                    ))}
                </ul>
            ) : (
                <div className="col__empty">Nothing here.</div>
            )}
        </CardBody>
    </Card>
);

const CurriculumBrowser = () => {
    const [grade, setGrade] = useState(null);
    const [course, setCourse] = useState(null);
    const [unit, setUnit] = useState(null);

    const grades = useGrades();
    const courses = useCourses(grade);
    const units = useUnits(grade,course);
    const chapters = useChapters(grade, course, unit);

    const gradeItems = useMemo(
        () => (grades.data?.grades || []).map((row) => ({ id: row.gradeId, ...row })),
        [grades.data],
    );
    const courseItems = useMemo(
        () => (courses.data?.courses || []).map((row) => ({ id: row.courseId, ...row })),
        [courses.data],
    );
    const unitItems = useMemo(
        () => (units.data?.units || []).map((row) => ({ id: row.unitId, ...row })),
        [units.data],
    );
    const chapterItems = useMemo(
        () => (chapters.data?.chapters || []).map((row) => ({ id: row.chapterId, ...row })),
        [chapters.data],
    );

    if (grades.isError) {
        return (
            <EmptyState
                icon="!"
                title="Could not load curriculum"
                description={grades.error.message}
            />
        );
    }

    return (
        <>
            <PageHeader
                eyebrow="Curriculum"
                title="Browse curriculum"
                description="Grades → Courses → Units → Chapters. Click a chapter to open its curriculum entry (with planners and assessments)."
            />
            <div className="curriculum-grid">
                <Column
                    title="Grades"
                    hint={grades.data ? `${grades.data.totalGrades} grades` : ""}
                    items={gradeItems}
                    active={grade}
                    onSelect={(value) => {
                        setGrade(value);
                        setCourse(null);
                        setUnit(null);
                    }}
                    isLoading={grades.isLoading}
                    renderItem={(row) => (
                        <>
                            <span>{row.gradeName}</span>
                            <span className="col__meta">{row.numberOfCourses} courses</span>
                        </>
                    )}
                />
                <Column
                    title="Courses"
                    hint={course === null ? "Pick a grade" : `${courseItems.length} courses`}
                    items={grade ? courseItems : []}
                    active={course}
                    onSelect={(value) => {
                        setCourse(value);
                        setUnit(null);
                    }}
                    isLoading={grade && courses.isLoading}
                    renderItem={(row) => (
                        <>
                            <span>{row.courseName}</span>
                            <span className="col__meta">{row.numberOfUnits} units</span>
                        </>
                    )}
                />
                <Column
                    title="Units"
                    hint={unit === null ? "Pick a course" : `${unitItems.length} units`}
                    items={course ? unitItems : []}
                    active={unit}
                    onSelect={setUnit}
                    isLoading={course && units.isLoading}
                    renderItem={(row) => (
                        <>
                            <span>{row.unitName}</span>
                            <span className="col__meta">{row.numberOfChapters} chapters</span>
                        </>
                    )}
                />
                <Column
                    title="Chapters"
                    hint={unit ? `${chapterItems.length} chapters` : "Pick a unit"}
                    items={unit ? chapterItems : []}
                    active={null}
                    onSelect={() => {}}
                    isLoading={unit && chapters.isLoading}
                    renderItem={(row) => (
                        <span>{row.chapterName}</span>
                    )}
                />
            </div>
        </>
    );
};

export default CurriculumBrowser;
