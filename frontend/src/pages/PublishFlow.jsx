import { useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import Badge from "../components/ui/Badge.jsx";
import Button from "../components/ui/Button.jsx";
import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import ConfirmDialog from "../components/ui/ConfirmDialog.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import StatusPill from "../components/ui/StatusPill.jsx";
import {
    useAssessment,
    useAssessmentQuestions,
    usePublishAssessment,
} from "../hooks/useAssessments.js";
import "./PublishFlow.css";

const PublishFlow = () => {
    const { assessmentId } = useParams();
    const navigate = useNavigate();
    const assessment = useAssessment(assessmentId);
    const questions = useAssessmentQuestions(assessmentId);
    const publish = usePublishAssessment(assessmentId);
    const [confirm, setConfirm] = useState(false);

    const preview = useMemo(() => {
        if (!assessment.data) return null;
        return { ...assessment.data, questions: questions.data || [] };
    }, [assessment.data, questions.data]);

    if (assessment.isLoading || questions.isLoading)
        return <Spinner label="Preparing publish preview…" size="lg" />;
    if (!assessment.data)
        return (
            <EmptyState
                icon="!"
                title="Assessment not found"
                description={assessment.error?.message}
            />
        );

    const alreadyPublished = assessment.data.status === "Published";

    return (
        <>
            <PageHeader
                eyebrow="Publish"
                title="Publish to portal"
                description="Preview the exact JSON that will be POSTed to the portal. When PORTAL_PUBLISH_URL is not configured the payload is signed and written to disk as a demo artifact."
                actions={
                    <>
                        <Link to={`/assessments/${assessmentId}`}>
                            <Button variant="secondary">Back to editor</Button>
                        </Link>
                        <Button variant={alreadyPublished ? "success" : "primary"} onClick={() => setConfirm(true)}>
                            {alreadyPublished ? "Republish" : "Publish now"}
                        </Button>
                    </>
                }
            />

            <div className="publish-flow__grid">
                <Card padding="none">
                    <CardHeader>
                        <div>
                            <div className="publish-flow__title">Assessment overview</div>
                            <div className="publish-flow__hint">Snapshot the portal will receive.</div>
                        </div>
                        <StatusPill status={assessment.data.status} />
                    </CardHeader>
                    <CardBody className="publish-flow__overview">
                        <dl>
                            <dt>Chapter</dt><dd>{assessment.data.chapterName}</dd>
                            <dt>Grade</dt><dd>{assessment.data.grade}</dd>
                            <dt>Version</dt><dd>v{assessment.data.version}</dd>
                            <dt>Total marks</dt><dd>{assessment.data.totalMarks}</dd>
                            <dt>Questions</dt><dd>{questions.data?.length ?? 0}</dd>
                            <dt>Learning outcomes</dt>
                            <dd>{assessment.data.learningOutcomes.join(" · ")}</dd>
                        </dl>
                        {assessment.data.publishDigest && (
                            <div className="publish-flow__digest">
                                <Badge tone="success">SHA-256</Badge>
                                <code>{assessment.data.publishDigest}</code>
                            </div>
                        )}
                        {assessment.data.publishTarget && (
                            <div className="publish-flow__target">
                                <span>Last target:</span>
                                <code>{assessment.data.publishTarget}</code>
                            </div>
                        )}
                    </CardBody>
                </Card>

                <Card padding="none">
                    <CardHeader>
                        <div>
                            <div className="publish-flow__title">Portal payload</div>
                            <div className="publish-flow__hint">POST body — JSON.</div>
                        </div>
                    </CardHeader>
                    <CardBody>
                        <pre className="publish-flow__json">
                            {JSON.stringify(preview, null, 2)}
                        </pre>
                    </CardBody>
                </Card>
            </div>

            <ConfirmDialog
                open={confirm}
                title={alreadyPublished ? "Republish assessment?" : "Publish assessment?"}
                description="This calls the portal API (or writes a signed JSON artifact when no URL is configured). Signed with SHA-256; the digest is recorded on the assessment."
                confirmLabel={alreadyPublished ? "Republish" : "Publish"}
                onCancel={() => setConfirm(false)}
                onConfirm={async () => {
                    await publish.mutateAsync();
                    setConfirm(false);
                    navigate(`/assessments/${assessmentId}`);
                }}
                loading={publish.isPending}
            />
        </>
    );
};

export default PublishFlow;
