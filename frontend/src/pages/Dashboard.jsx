import { Link } from "react-router-dom";

import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import StatTile from "../components/ui/StatTile.jsx";
import StatusPill from "../components/ui/StatusPill.jsx";
import Table from "../components/ui/Table.jsx";
import Button from "../components/ui/Button.jsx";
import { useDashboardSummary } from "../hooks/useDashboard.js";
import { formatDateTime, formatVersion } from "../lib/format.js";
import "./Dashboard.css";

const Dashboard = () => {
    const { data, isLoading, isError, error } = useDashboardSummary();

    if (isLoading) return <Spinner label="Loading dashboard…" size="lg" />;
    if (isError)
        return (
            <EmptyState
                icon="!"
                title="Could not load dashboard"
                description={error.message}
            />
        );

    const { totals, statusBreakdown, averageTotalMarks, recentAssessments, recentSubmissions } = data;

    return (
        <>
            <PageHeader
                eyebrow="Overview"
                title="Assessment Automation Dashboard"
                description="A single view of the pipeline — generated assessments, published portal drops, student submissions and planner-change propagation."
                actions={
                    <>
                        <Button variant="secondary" as={Link} onClick={() => (window.location.href = "/planners")}>
                            Browse planners
                        </Button>
                        <Button variant="primary" onClick={() => (window.location.href = "/planners")}>
                            Generate assessment
                        </Button>
                    </>
                }
            />

            <section className="dashboard__stats">
                <StatTile
                    label="Assessments"
                    value={totals.assessments}
                    hint="all statuses"
                    icon="❑"
                />
                <StatTile
                    tone="success"
                    label="Published"
                    value={totals.published}
                    hint="live in portal"
                    icon="↗"
                />
                <StatTile
                    tone="warning"
                    label="Outdated"
                    value={totals.outdated}
                    hint="pending regeneration"
                    icon="!"
                />
                <StatTile
                    tone="info"
                    label="Submissions"
                    value={totals.submissions}
                    hint="hard-locked snapshots"
                    icon="✓"
                />
                <StatTile
                    tone="danger"
                    label="Propagation events"
                    value={totals.propagationEvents}
                    hint="planner-outcome changes"
                    icon="↻"
                />
                <StatTile
                    label="Avg. marks"
                    value={averageTotalMarks}
                    hint="per assessment"
                    icon="Σ"
                />
            </section>

            <section className="dashboard__grid">
                <Card padding="none">
                    <CardHeader>
                        <div>
                            <div className="dashboard__section-title">Status breakdown</div>
                            <div className="dashboard__section-hint">Distribution of assessments by lifecycle state.</div>
                        </div>
                    </CardHeader>
                    <CardBody>
                        <div className="dashboard__status-grid">
                            {Object.entries(statusBreakdown).map(([status, count]) => (
                                <div key={status} className="dashboard__status-row">
                                    <StatusPill status={status} />
                                    <span className="dashboard__status-count">{count}</span>
                                </div>
                            ))}
                        </div>
                    </CardBody>
                </Card>

                <Card padding="none">
                    <CardHeader>
                        <div>
                            <div className="dashboard__section-title">Recent assessments</div>
                            <div className="dashboard__section-hint">The five most recently created.</div>
                        </div>
                        <Link to="/assessments">View all →</Link>
                    </CardHeader>
                    <CardBody>
                        <Table
                            emptyLabel="No assessments yet — generate one from a planner to get started."
                            columns={[
                                {
                                    key: "chapterName",
                                    header: "Chapter",
                                    render: (row) => (
                                        <Link to={`/assessments/${row.assessmentId}`}>{row.chapterName || "—"}</Link>
                                    ),
                                },
                                { key: "grade", header: "Grade" },
                                {
                                    key: "status",
                                    header: "Status",
                                    render: (row) => <StatusPill status={row.status} />,
                                },
                                {
                                    key: "version",
                                    header: "Version",
                                    render: (row) => formatVersion(row.version),
                                },
                                {
                                    key: "generatedOn",
                                    header: "Created",
                                    render: (row) => formatDateTime(row.generatedOn),
                                },
                            ]}
                            rows={recentAssessments || []}
                            getRowKey={(row) => row.assessmentId}
                        />
                    </CardBody>
                </Card>

                <Card padding="none">
                    <CardHeader>
                        <div>
                            <div className="dashboard__section-title">Recent submissions</div>
                            <div className="dashboard__section-hint">Immutable snapshots preserved from time of submit.</div>
                        </div>
                    </CardHeader>
                    <CardBody>
                        <Table
                            emptyLabel="No submissions yet."
                            columns={[
                                { key: "studentName", header: "Student", render: (row) => row.studentName || row.studentId },
                                {
                                    key: "score",
                                    header: "Score",
                                    render: (row) => `${row.score}/${row.maxScore}`,
                                },
                                {
                                    key: "submittedOn",
                                    header: "Submitted",
                                    render: (row) => formatDateTime(row.submittedOn),
                                },
                            ]}
                            rows={recentSubmissions || []}
                            getRowKey={(row) => row.submissionId}
                        />
                    </CardBody>
                </Card>
            </section>
        </>
    );
};

export default Dashboard;
