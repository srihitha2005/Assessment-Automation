import { useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import Badge from "../components/ui/Badge.jsx";
import Button from "../components/ui/Button.jsx";
import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import Modal from "../components/ui/Modal.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import StatusPill from "../components/ui/StatusPill.jsx";
import Table from "../components/ui/Table.jsx";
import { FormField, Textarea } from "../components/ui/FormField.jsx";
import { useGenerateAssessment } from "../hooks/useAssessments.js";
import { usePlanner } from "../hooks/useCurriculum.js";
import { useUpdatePlannerOutcomes } from "../hooks/usePropagation.js";
import { formatDateTime, formatVersion } from "../lib/format.js";
import "./PlannerDetail.css";

const PlannerDetail = () => {
    const { plannerId } = useParams();
    const navigate = useNavigate();

    const { data: planner, isLoading, isError, error } = usePlanner(plannerId);
    const generate = useGenerateAssessment();
    const updateOutcomes = useUpdatePlannerOutcomes();

    const [prompt, setPrompt] = useState("");
    const [outcomesOpen, setOutcomesOpen] = useState(false);
    const [outcomeDraft, setOutcomeDraft] = useState("");

    const outcomesList = useMemo(
        () => outcomeDraft.split("\n").map((line) => line.trim()).filter(Boolean),
        [outcomeDraft],
    );

    if (isLoading) return <Spinner label="Loading planner…" size="lg" />;
    if (isError || !planner)
        return (
            <EmptyState
                icon="!"
                title="Planner not found"
                description={error?.message || "The requested planner does not exist."}
                action={
                    <Button variant="secondary" onClick={() => navigate("/planners")}>
                        Back to planners
                    </Button>
                }
            />
        );

    const handleGenerate = async () => {
        try {
            const result = await generate.mutateAsync({
                plannerId,
                prompt: prompt.trim() || undefined,
            });
            navigate(`/assessments/${result.assessmentId}`);
        } catch (_) {
            /* toast handled in hook */
        }
    };

    return (
        <>
            <PageHeader
                eyebrow={`Planner · ${planner.plannerId}`}
                title={planner.plannerName}
                description={`${planner.grade || "Grade"} — ${planner.courseName || ""} · ${planner.unitName || ""} · ${planner.chapterName || ""}`}
                actions={
                    <>
                        <Button
                            variant="secondary"
                            onClick={() => {
                                setOutcomeDraft(planner.learningOutcomes.join("\n"));
                                setOutcomesOpen(true);
                            }}
                        >
                            Edit outcomes (simulate)
                        </Button>
                        <Button variant="primary" onClick={handleGenerate} loading={generate.isPending}>
                            Generate assessment
                        </Button>
                    </>
                }
            />

            <div className="planner-detail__grid">
                <Card padding="none">
                    <CardHeader>
                        <div>
                            <div className="planner-detail__section-title">Learning outcomes</div>
                            <div className="planner-detail__section-hint">
                                These drive difficulty, Bloom, and question-type balance.
                            </div>
                        </div>
                        <Badge tone="brand">{planner.learningOutcomes.length}</Badge>
                    </CardHeader>
                    <CardBody>
                        {planner.learningOutcomes.length > 0 ? (
                            <ul className="planner-detail__outcomes">
                                {planner.learningOutcomes.map((outcome, index) => (
                                    <li key={outcome}>
                                        <span className="planner-detail__outcome-index">{index + 1}</span>
                                        {outcome}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <div className="planner-detail__empty-outcomes">
                                Open the parsed planner document to load its learning outcomes.
                            </div>
                        )}
                    </CardBody>
                </Card>

                <Card padding="none">
                    <CardHeader>
                        <div>
                            <div className="planner-detail__section-title">Teacher guidance (optional)</div>
                            <div className="planner-detail__section-hint">
                                Steer generation — “more application-based questions”, “less recall”, etc.
                            </div>
                        </div>
                    </CardHeader>
                    <CardBody>
                        <FormField
                            label="Prompt"
                            hint="Leave empty for balanced defaults."
                        >
                            <Textarea
                                placeholder="Emphasise diagram-based questions this time."
                                value={prompt}
                                onChange={(event) => setPrompt(event.target.value)}
                            />
                        </FormField>
                        <div className="planner-detail__actions">
                            <Button variant="primary" onClick={handleGenerate} loading={generate.isPending}>
                                Generate assessment
                            </Button>
                        </div>
                    </CardBody>
                </Card>

                <Card padding="none" className="planner-detail__wide">
                    <CardHeader>
                        <div>
                            <div className="planner-detail__section-title">Previous assessments</div>
                            <div className="planner-detail__section-hint">
                                Every generation for this planner. New runs exclude questions used before.
                            </div>
                        </div>
                        <Link to="/assessments">All assessments →</Link>
                    </CardHeader>
                    <CardBody>
                        <Table
                            emptyLabel="No assessments generated for this planner yet."
                            columns={[
                                {
                                    key: "assessmentNumber",
                                    header: "#",
                                    render: (row) => (
                                        <Link to={`/assessments/${row.assessmentId}`}>#{row.assessmentNumber}</Link>
                                    ),
                                },
                                {
                                    key: "status",
                                    header: "Status",
                                    render: (row) => <StatusPill status={row.status} />,
                                },
                                { key: "questionCount", header: "Questions" },
                                { key: "totalMarks", header: "Marks" },
                                { key: "version", header: "Version", render: (row) => formatVersion(row.version) },
                                {
                                    key: "generatedOn",
                                    header: "Generated",
                                    render: (row) => formatDateTime(row.generatedOn),
                                },
                            ]}
                            rows={planner.assessments || []}
                            getRowKey={(row) => row.assessmentId}
                        />
                    </CardBody>
                </Card>
            </div>

            <Modal
                open={outcomesOpen}
                title="Simulate planner outcome change"
                description="Edit the outcomes below and save to record a propagation event. Published assessments tied to this planner become 'Outdated'."
                size="md"
                onClose={() => setOutcomesOpen(false)}
                footer={
                    <>
                        <Button variant="ghost" onClick={() => setOutcomesOpen(false)}>Cancel</Button>
                        <Button
                            variant="primary"
                            loading={updateOutcomes.isPending}
                            onClick={async () => {
                                await updateOutcomes.mutateAsync({
                                    plannerId,
                                    payload: { learningOutcomes: outcomesList },
                                });
                                setOutcomesOpen(false);
                            }}
                        >
                            Save outcomes
                        </Button>
                    </>
                }
            >
                <FormField
                    label="Learning outcomes (one per line)"
                    hint={`${outcomesList.length} outcome(s) will be saved.`}
                >
                    <Textarea
                        rows={8}
                        value={outcomeDraft}
                        onChange={(event) => setOutcomeDraft(event.target.value)}
                    />
                </FormField>
            </Modal>
        </>
    );
};

export default PlannerDetail;
