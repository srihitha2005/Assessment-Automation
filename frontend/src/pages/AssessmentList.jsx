import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import Badge from "../components/ui/Badge.jsx";
import Button from "../components/ui/Button.jsx";
import Card, { CardBody } from "../components/ui/Card.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import StatusPill from "../components/ui/StatusPill.jsx";
import { Select, TextInput } from "../components/ui/FormField.jsx";
import { STATUS_TOKENS } from "../lib/constants.js";
import { useAssessments } from "../hooks/useAssessments.js";
import { formatDateTime, formatVersion, pluralise } from "../lib/format.js";
import "./AssessmentList.css";

const AssessmentList = () => {
    const { data, isLoading, isError, error } = useAssessments();
    const [query, setQuery] = useState("");
    const [status, setStatus] = useState("");

    const rows = useMemo(() => {
        const list = data || [];
        return list.filter((item) => {
            const matchesQuery =
                !query ||
                item.chapterName?.toLowerCase().includes(query.toLowerCase()) ||
                item.grade?.toLowerCase().includes(query.toLowerCase());
            const matchesStatus = !status || item.status === status;
            return matchesQuery && matchesStatus;
        });
    }, [data, query, status]);

    if (isLoading) return <Spinner label="Loading assessments…" size="lg" />;
    if (isError) return <EmptyState icon="!" title="Could not load assessments" description={error.message} />;

    return (
        <>
            <PageHeader
                eyebrow="Assessments"
                title="Assessment library"
                description="Every generated, parsed, published and outdated assessment across all planners."
                actions={
                    <>
                        <TextInput
                            placeholder="Search chapter or grade…"
                            value={query}
                            onChange={(event) => setQuery(event.target.value)}
                            style={{ minWidth: 220 }}
                        />
                        <Select
                            value={status}
                            onChange={(event) => setStatus(event.target.value)}
                            style={{ minWidth: 160 }}
                        >
                            <option value="">All statuses</option>
                            {Object.keys(STATUS_TOKENS).map((key) => (
                                <option key={key} value={key}>
                                    {STATUS_TOKENS[key].label}
                                </option>
                            ))}
                        </Select>
                    </>
                }
            />

            <div className="assessments__meta">
                {pluralise(rows.length, "assessment")} shown.
            </div>

            {rows.length === 0 ? (
                <EmptyState
                    icon="◍"
                    title="No assessments to show"
                    description="Adjust your filters or generate one from a planner."
                    action={
                        <Button variant="primary" onClick={() => (window.location.href = "/planners")}>
                            Go to planners
                        </Button>
                    }
                />
            ) : (
                <div className="assessment-grid">
                    {rows.map((row) => (
                        <Card key={row.assessmentId} padding="none" className="assessment-tile">
                            <CardBody>
                                <div className="assessment-tile__header">
                                    <StatusPill status={row.status} />
                                    <Badge tone="neutral">{formatVersion(row.version)}</Badge>
                                </div>
                                <Link
                                    className="assessment-tile__title"
                                    to={`/assessments/${row.assessmentId}`}
                                >
                                    {row.chapterName || "—"}
                                </Link>
                                <div className="assessment-tile__meta">
                                    {row.grade} · {row.courseName || "—"}
                                </div>

                                <dl className="assessment-tile__stats">
                                    <div>
                                        <dt>Questions</dt>
                                        <dd>{row.questionCount}</dd>
                                    </div>
                                    <div>
                                        <dt>Marks</dt>
                                        <dd>{row.totalMarks}</dd>
                                    </div>
                                    <div>
                                        <dt>Outcomes</dt>
                                        <dd>{row.learningOutcomeCount}</dd>
                                    </div>
                                    <div>
                                        <dt>Number</dt>
                                        <dd>#{row.assessmentNumber}</dd>
                                    </div>
                                </dl>

                                <div className="assessment-tile__footer">
                                    <span className="assessment-tile__date">
                                        {formatDateTime(row.generatedOn)}
                                    </span>
                                    <Link
                                        className="assessment-tile__link"
                                        to={`/assessments/${row.assessmentId}`}
                                    >
                                        Open →
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

export default AssessmentList;
