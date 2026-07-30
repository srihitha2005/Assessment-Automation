import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Badge from "../ui/Badge.jsx";
import Button from "../ui/Button.jsx";
import ConfirmDialog from "../ui/ConfirmDialog.jsx";
import Modal from "../ui/Modal.jsx";
import StatusPill from "../ui/StatusPill.jsx";
import { FormField, Textarea } from "../ui/FormField.jsx";
import { assessmentApi } from "../../lib/api.js";
import {
    useDeleteAssessment,
    useParseAssessment,
    useRegenerateAssessment,
} from "../../hooks/useAssessments.js";
import { formatDateTime, formatVersion } from "../../lib/format.js";
import "./AssessmentToolbar.css";

const AssessmentToolbar = ({ assessment }) => {
    const navigate = useNavigate();
    const regenerate = useRegenerateAssessment(assessment.assessmentId);
    const parse = useParseAssessment(assessment.assessmentId);
    const remove = useDeleteAssessment();

    const [regenOpen, setRegenOpen] = useState(false);
    const [prompt, setPrompt] = useState("");
    const [confirmDelete, setConfirmDelete] = useState(false);

    const isPublished = assessment.status === "Published";

    return (
        <>
            <div className="assessment-toolbar">
                <div className="assessment-toolbar__meta">
                    <div>
                        <div className="assessment-toolbar__eyebrow">
                            Assessment #{assessment.assessmentNumber} · Planner {assessment.plannerId}
                        </div>
                        <h1 className="assessment-toolbar__title">{assessment.chapterName}</h1>
                        <div className="assessment-toolbar__subline">
                            <StatusPill status={assessment.status} />
                            <Badge tone="neutral">{formatVersion(assessment.version)}</Badge>
                            <Badge tone="brand">{assessment.grade}</Badge>
                            <span className="assessment-toolbar__hint">
                                {assessment.questionCount} questions · {assessment.totalMarks} marks
                            </span>
                        </div>
                        <div className="assessment-toolbar__timestamps">
                            Generated {formatDateTime(assessment.generatedOn)} by {assessment.generatedBy || "SYSTEM"}
                            {" · "}Updated {formatDateTime(assessment.updatedOn)} by {assessment.updatedBy || "SYSTEM"}
                        </div>
                    </div>
                </div>

                <div className="assessment-toolbar__actions">
                    <Button
                        variant="secondary"
                        onClick={() => window.open(assessmentApi.docxUrl(assessment.assessmentId), "_blank")}
                    >
                        Download DOCX
                    </Button>
                    <Button
                        variant="secondary"
                        onClick={() => window.open(assessmentApi.pdfUrl(assessment.assessmentId), "_blank")}
                    >
                        Download PDF
                    </Button>
                    <Button
                        variant="secondary"
                        onClick={() => parse.mutate()}
                        loading={parse.isPending}
                    >
                        Parse DOCX
                    </Button>
                    <Button variant="secondary" onClick={() => setRegenOpen(true)}>
                        Regenerate
                    </Button>
                    <Link to={`/assessments/${assessment.assessmentId}/versions`}>
                        <Button variant="ghost">Version history</Button>
                    </Link>
                    <Link to={`/assessments/${assessment.assessmentId}/publish`}>
                        <Button variant={isPublished ? "success" : "primary"}>
                            {isPublished ? "Republish" : "Publish"}
                        </Button>
                    </Link>
                    <Button variant="danger" onClick={() => setConfirmDelete(true)}>
                        Delete
                    </Button>
                </div>

                {assessment.validationReport?.missingOutcomes?.length ? (
                    <div className="assessment-toolbar__warning">
                        Missing coverage for {assessment.validationReport.missingOutcomes.length} learning outcome(s).
                    </div>
                ) : null}

                {assessment.validationReport?.needsReview ? (
                    <div className="assessment-toolbar__warning">
                        Some questions were placeholder-generated — flagged for teacher review.
                    </div>
                ) : null}
            </div>

            <Modal
                open={regenOpen}
                title="Regenerate this assessment"
                description="Replaces every question. Historical submissions keep their locked snapshots."
                size="md"
                onClose={() => setRegenOpen(false)}
                footer={
                    <>
                        <Button variant="ghost" onClick={() => setRegenOpen(false)}>Cancel</Button>
                        <Button
                            variant="primary"
                            loading={regenerate.isPending}
                            onClick={async () => {
                                await regenerate.mutateAsync({ prompt: prompt.trim() || undefined });
                                setRegenOpen(false);
                                setPrompt("");
                            }}
                        >
                            Regenerate
                        </Button>
                    </>
                }
            >
                <FormField label="Teacher guidance (optional)" hint="e.g. more Bloom-Analyze questions.">
                    <Textarea
                        value={prompt}
                        onChange={(event) => setPrompt(event.target.value)}
                        placeholder="Emphasise application-level questions."
                    />
                </FormField>
            </Modal>

            <ConfirmDialog
                open={confirmDelete}
                title="Delete assessment?"
                description="This removes the assessment and every question. Submissions retain their locked snapshots. This cannot be undone."
                tone="danger"
                confirmLabel="Delete"
                onCancel={() => setConfirmDelete(false)}
                onConfirm={async () => {
                    await remove.mutateAsync(assessment.assessmentId);
                    setConfirmDelete(false);
                    navigate("/assessments");
                }}
                loading={remove.isPending}
            />
        </>
    );
};

export default AssessmentToolbar;
