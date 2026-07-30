import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import Badge from "../components/ui/Badge.jsx";
import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import { TextInput } from "../components/ui/FormField.jsx";
import { usePlanners } from "../hooks/useCurriculum.js";
import "./PlannerBrowser.css";

const PlannerBrowser = () => {
    const { data, isLoading, isError, error } = usePlanners();
    const [query, setQuery] = useState("");

    const filtered = useMemo(() => {
        const rows = data?.planners || [];
        const q = query.trim().toLowerCase();
        if (!q) return rows;
        return rows.filter(
            (row) =>
                row.plannerName?.toLowerCase().includes(q) ||
                row.chapterName?.toLowerCase().includes(q) ||
                row.courseName?.toLowerCase().includes(q),
        );
    }, [data, query]);

    if (isLoading) return <Spinner label="Loading planners…" size="lg" />;
    if (isError) return <EmptyState icon="!" title="Could not load planners" description={error.message} />;

    return (
        <>
            <PageHeader
                eyebrow="Planners"
                title="Planners"
                description="Each planner ties a chapter to the learning outcomes teachers want covered. Click a planner to generate a new assessment against those outcomes."
                actions={
                    <TextInput
                        placeholder="Search planners, chapters, courses…"
                        value={query}
                        onChange={(event) => setQuery(event.target.value)}
                        style={{ minWidth: 260 }}
                    />
                }
            />

            {filtered.length === 0 ? (
                <EmptyState
                    icon="◍"
                    title="No planners match your search"
                    description="Try a different query or clear the search."
                />
            ) : (
                <div className="planner-grid">
                    {filtered.map((planner) => (
                        <Card key={planner.plannerId} padding="none" className="planner-card">
                            <CardHeader>
                                <div>
                                    <div className="planner-card__title">{planner.plannerName}</div>
                                    <div className="planner-card__meta">
                                        {planner.grade} · {planner.chapterName || "no chapter"}
                                    </div>
                                </div>
                                <Badge tone="brand">{planner.plannerId}</Badge>
                            </CardHeader>
                            <CardBody>
                                <div className="planner-card__section">
                                    <div className="planner-card__label">Course / Unit</div>
                                    <div>{planner.courseName} · {planner.unitName}</div>
                                </div>
                                <div className="planner-card__section">
                                    <div className="planner-card__label">
                                        Learning outcomes ({planner.learningOutcomes.length})
                                    </div>
                                    <ul className="planner-card__outcomes">
                                        {planner.learningOutcomes.map((outcome) => (
                                            <li key={outcome}>{outcome}</li>
                                        ))}
                                    </ul>
                                </div>
                                <div className="planner-card__footer">
                                    <span className="planner-card__count">
                                        {planner.numberOfAssessments} assessment(s)
                                    </span>
                                    <Link to={`/planners/${planner.plannerId}`} className="planner-card__link">
                                        Open planner →
                                    </Link>
                                </div>
                            </CardBody>
                        </Card>
                    ))}
                </div>
            )}
        </>
    );
};

export default PlannerBrowser;
