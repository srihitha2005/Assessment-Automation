import { useState } from "react";
import { Link, useParams } from "react-router-dom";

import Badge from "../components/ui/Badge.jsx";
import Button from "../components/ui/Button.jsx";
import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import ConfirmDialog from "../components/ui/ConfirmDialog.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import {
    useAssessment,
    useAssessmentVersions,
    useRollbackAssessment,
} from "../hooks/useAssessments.js";
import { formatDateTime } from "../lib/format.js";
import "./VersionHistory.css";

const VersionHistory = () => {
    const { assessmentId } = useParams();
    const assessment = useAssessment(assessmentId);
    const versions = useAssessmentVersions(assessmentId);
    const rollback = useRollbackAssessment(assessmentId);
    const [target, setTarget] = useState(null);

    if (assessment.isLoading || versions.isLoading)
        return <Spinner label="Loading version history…" size="lg" />;

    if (assessment.isError || !assessment.data)
        return (
            <EmptyState
                icon="!"
                title="Assessment not found"
                description={assessment.error?.message || "It may have been deleted."}
            />
        );

    const items = versions.data || [];

    return (
        <>
            <PageHeader
                eyebrow={`Assessment · ${assessment.data.chapterName}`}
                title="Version history"
                description="Every mutation writes an immutable snapshot. Rollback re-materialises the entire assessment (including questions) from any snapshot."
                actions={
                    <Link to={`/assessments/${assessmentId}`}>
                        <Button variant="secondary">Back to editor</Button>
                    </Link>
                }
            />

            {items.length === 0 ? (
                <EmptyState
                    icon="↻"
                    title="No version history yet"
                    description="Edit or regenerate the assessment to create the first snapshot."
                />
            ) : (
                <Card padding="none">
                    <CardHeader>
                        <div>
                            <div className="version-history__title">Timeline</div>
                            <div className="version-history__hint">Newest first.</div>
                        </div>
                        <Badge tone="brand">Current v{assessment.data.version}</Badge>
                    </CardHeader>
                    <CardBody>
                        <ol className="version-history__list">
                            {items.map((item) => (
                                <li key={`${item.version}-${item.createdOn}`}>
                                    <div className="version-history__marker">v{item.version}</div>
                                    <div className="version-history__body">
                                        <div className="version-history__row">
                                            <Badge tone="info">{item.action}</Badge>
                                            <span className="version-history__meta">
                                                {formatDateTime(item.createdOn)} · {item.createdBy}
                                            </span>
                                        </div>
                                        <div className="version-history__actions">
                                            <Button
                                                variant="secondary"
                                                size="sm"
                                                onClick={() => setTarget(item)}
                                                disabled={item.version === assessment.data.version}
                                            >
                                                {item.version === assessment.data.version
                                                    ? "Current"
                                                    : `Rollback to v${item.version}`}
                                            </Button>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ol>
                    </CardBody>
                </Card>
            )}

            <ConfirmDialog
                open={Boolean(target)}
                title={target ? `Rollback to v${target.version}?` : ""}
                description="A new snapshot will be recorded first, so this action is itself reversible."
                confirmLabel="Rollback"
                onCancel={() => setTarget(null)}
                onConfirm={async () => {
                    await rollback.mutateAsync({ version: target.version });
                    setTarget(null);
                }}
                loading={rollback.isPending}
            />
        </>
    );
};

export default VersionHistory;
