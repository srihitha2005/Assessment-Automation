import { useState } from "react";

import Badge from "../ui/Badge.jsx";
import Button from "../ui/Button.jsx";
import Card, { CardBody, CardHeader } from "../ui/Card.jsx";
import Modal from "../ui/Modal.jsx";
import Table from "../ui/Table.jsx";
import { FormField, TextInput } from "../ui/FormField.jsx";
import { useCreateSubmission, useSubmissions } from "../../hooks/useSubmissions.js";
import { formatDateTime } from "../../lib/format.js";
import "./SubmissionPanel.css";

const SubmissionPanel = ({ assessmentId, questions }) => {
    const submissions = useSubmissions(assessmentId);
    const create = useCreateSubmission(assessmentId);

    const [open, setOpen] = useState(false);
    const [studentName, setStudentName] = useState("");
    const [studentId, setStudentId] = useState("");
    const [answers, setAnswers] = useState(() =>
        Object.fromEntries((questions || []).map((question) => [question.questionNumber, ""]))
    );

    const submit = async () => {
        await create.mutateAsync({
            studentId: studentId || `stu-${Date.now()}`,
            studentName: studentName || null,
            answers: Object.entries(answers).map(([questionNumber, answer]) => ({
                questionNumber: Number(questionNumber),
                answer,
            })),
        });
        setOpen(false);
        setStudentName("");
        setStudentId("");
        setAnswers(Object.fromEntries((questions || []).map((question) => [question.questionNumber, ""])));
    };

    return (
        <Card padding="none">
            <CardHeader>
                <div>
                    <div className="submission-panel__title">Submissions</div>
                    <div className="submission-panel__hint">
                        Each submission freezes the assessment version into a locked snapshot.
                    </div>
                </div>
                <Button variant="secondary" onClick={() => setOpen(true)}>
                    Record submission
                </Button>
            </CardHeader>
            <CardBody>
                <Table
                    emptyLabel="No submissions yet."
                    columns={[
                        {
                            key: "student",
                            header: "Student",
                            render: (row) => (
                                <div>
                                    <div>{row.studentName || row.studentId}</div>
                                    <div className="submission-panel__id">{row.studentId}</div>
                                </div>
                            ),
                        },
                        {
                            key: "score",
                            header: "Score",
                            render: (row) => `${row.score} / ${row.maxScore}`,
                        },
                        {
                            key: "assessmentVersion",
                            header: "Locked version",
                            render: (row) => <Badge tone="brand">v{row.assessmentVersion}</Badge>,
                        },
                        {
                            key: "submittedOn",
                            header: "Submitted",
                            render: (row) => formatDateTime(row.submittedOn),
                        },
                    ]}
                    rows={submissions.data || []}
                    getRowKey={(row) => row.submissionId}
                />
            </CardBody>

            <Modal
                open={open}
                title="Record student submission"
                description="For demo — enter one answer per question, exact-match auto-scoring."
                size="lg"
                onClose={() => setOpen(false)}
                footer={
                    <>
                        <Button variant="ghost" onClick={() => setOpen(false)}>Cancel</Button>
                        <Button variant="primary" onClick={submit} loading={create.isPending}>
                            Record
                        </Button>
                    </>
                }
            >
                <div className="submission-panel__form">
                    <div className="submission-panel__row">
                        <FormField label="Student ID" hint="Any unique identifier.">
                            <TextInput value={studentId} onChange={(event) => setStudentId(event.target.value)} placeholder="stu-100" />
                        </FormField>
                        <FormField label="Name (optional)">
                            <TextInput value={studentName} onChange={(event) => setStudentName(event.target.value)} placeholder="Alice" />
                        </FormField>
                    </div>
                    {(questions || []).map((question) => (
                        <FormField
                            key={question.questionId}
                            label={`Q${question.questionNumber}. ${question.question.slice(0, 80)}${question.question.length > 80 ? "…" : ""}`}
                        >
                            <TextInput
                                placeholder="Student's answer"
                                value={answers[question.questionNumber] || ""}
                                onChange={(event) =>
                                    setAnswers({ ...answers, [question.questionNumber]: event.target.value })
                                }
                            />
                        </FormField>
                    ))}
                </div>
            </Modal>
        </Card>
    );
};

export default SubmissionPanel;
