import { useMemo, useState } from "react";

import Badge from "../components/ui/Badge.jsx";
import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import { TextInput } from "../components/ui/FormField.jsx";
import { usePlanners } from "../hooks/useCurriculum.js";
import "./QuestionBankBrowser.css";

const QuestionBankBrowser = () => {
    const planners = usePlanners();
    const [query, setQuery] = useState("");

    const chapters = useMemo(() => {
        const map = new Map();
        (planners.data?.planners || []).forEach((planner) => {
            const key = `${planner.courseName}::${planner.unitName}::${planner.chapterName}`;
            if (!map.has(key)) {
                map.set(key, {
                    courseName: planner.courseName,
                    unitName: planner.unitName,
                    chapterName: planner.chapterName,
                    grade: planner.grade,
                    planners: [],
                });
            }
            map.get(key).planners.push(planner);
        });
        const rows = Array.from(map.values());
        if (!query) return rows;
        const q = query.toLowerCase();
        return rows.filter(
            (row) =>
                row.chapterName?.toLowerCase().includes(q) ||
                row.courseName?.toLowerCase().includes(q) ||
                row.unitName?.toLowerCase().includes(q),
        );
    }, [planners.data, query]);

    if (planners.isLoading) return <Spinner label="Loading question bank…" size="lg" />;
    if (planners.isError)
        return <EmptyState icon="!" title="Could not load question bank" description={planners.error.message} />;

    return (
        <>
            <PageHeader
                eyebrow="Question Bank"
                title="Chapters covered by the question bank"
                description="The pipeline seeds every assessment from the on-disk question bank first, and generates only the gaps with the local model."
                actions={
                    <TextInput
                        placeholder="Search chapters, units, courses…"
                        value={query}
                        onChange={(event) => setQuery(event.target.value)}
                        style={{ minWidth: 260 }}
                    />
                }
            />

            {chapters.length === 0 ? (
                <EmptyState icon="◍" title="No chapters match" description="Try a different query." />
            ) : (
                <div className="qb-grid">
                    {chapters.map((chapter) => (
                        <Card key={chapter.chapterName + chapter.unitName} padding="none">
                            <CardHeader>
                                <div>
                                    <div className="qb__title">{chapter.chapterName}</div>
                                    <div className="qb__meta">
                                        {chapter.grade} · {chapter.courseName} · {chapter.unitName}
                                    </div>
                                </div>
                                <Badge tone="brand">{chapter.planners.length} planner(s)</Badge>
                            </CardHeader>
                            <CardBody>
                                <ul className="qb__planners">
                                    {chapter.planners.map((planner) => (
                                        <li key={planner.plannerId}>
                                            <a href={`/planners/${planner.plannerId}`}>{planner.plannerName}</a>
                                            <span className="qb__outcomes">
                                                {planner.learningOutcomes.length} outcomes
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                            </CardBody>
                        </Card>
                    ))}
                </div>
            )}
        </>
    );
};

export default QuestionBankBrowser;
