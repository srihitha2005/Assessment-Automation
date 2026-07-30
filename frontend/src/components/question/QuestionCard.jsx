import { useState } from "react";

import Badge from "../ui/Badge.jsx";
import Button from "../ui/Button.jsx";
import Card, { CardBody } from "../ui/Card.jsx";
import ConfirmDialog from "../ui/ConfirmDialog.jsx";
import Modal from "../ui/Modal.jsx";
import { FormField, TextInput, Textarea } from "../ui/FormField.jsx";
import { DIFFICULTY_TOKENS } from "../../lib/constants.js";
import {
    useDeleteImage,
    useDeleteQuestion,
    useRegenerateAnswer,
    useRegenerateQuestion,
    useUpdateQuestion,
    useUploadImages,
} from "../../hooks/useQuestions.js";
import "./QuestionCard.css";

const QuestionCard = ({ question, assessmentId }) => {
    const [editing, setEditing] = useState(false);
    const [expanded, setExpanded] = useState(false);
    const [regenOpen, setRegenOpen] = useState(false);
    const [answerRegenOpen, setAnswerRegenOpen] = useState(false);
    const [confirmDelete, setConfirmDelete] = useState(false);
    const [prompt, setPrompt] = useState("");

    const [draft, setDraft] = useState({
        question: question.question,
        answer: question.answer,
        options: question.options,
        marks: question.marks,
    });

    const update = useUpdateQuestion(assessmentId);
    const regenerate = useRegenerateQuestion(assessmentId);
    const regenerateAnswer = useRegenerateAnswer(assessmentId);
    const remove = useDeleteQuestion(assessmentId);
    const upload = useUploadImages(assessmentId);
    const deleteImage = useDeleteImage(assessmentId);

    const startEdit = () => {
        setDraft({
            question: question.question,
            answer: question.answer,
            options: question.options,
            marks: question.marks,
        });
        setEditing(true);
    };

    const save = async () => {
        await update.mutateAsync({
            questionId: question.questionId,
            payload: {
                question: draft.question,
                answer: draft.answer,
                options: draft.options,
                marks: Number(draft.marks) || 1,
            },
        });
        setEditing(false);
    };

    return (
        <Card padding="none" className="question-card">
            <CardBody>
                <div className="question-card__header">
                    <div className="question-card__number">Q{question.questionNumber}</div>
                    <div className="question-card__badges">
                        <Badge tone="brand">{question.questionType}</Badge>
                        <Badge tone={DIFFICULTY_TOKENS[question.difficulty] || "neutral"}>
                            {question.difficulty}
                        </Badge>
                        <Badge tone="info">{question.bloomsLevel}</Badge>
                        <Badge tone="neutral">{question.marks} marks</Badge>
                        {question.needsReview && <Badge tone="warning">Needs review</Badge>}
                    </div>
                </div>

                {editing ? (
                    <div className="question-card__editor">
                        <FormField label="Question">
                            <Textarea
                                rows={2}
                                value={draft.question}
                                onChange={(event) => setDraft({ ...draft, question: event.target.value })}
                            />
                        </FormField>
                        <FormField label="Answer">
                            <Textarea
                                rows={2}
                                value={draft.answer}
                                onChange={(event) => setDraft({ ...draft, answer: event.target.value })}
                            />
                        </FormField>
                        {question.options?.length ? (
                            <FormField label="Options (one per line)">
                                <Textarea
                                    rows={question.options.length + 1}
                                    value={draft.options.join("\n")}
                                    onChange={(event) =>
                                        setDraft({
                                            ...draft,
                                            options: event.target.value
                                                .split("\n")
                                                .map((line) => line.trim())
                                                .filter(Boolean),
                                        })
                                    }
                                />
                            </FormField>
                        ) : null}
                        <FormField label="Marks">
                            <TextInput
                                type="number"
                                min={1}
                                max={20}
                                value={draft.marks}
                                onChange={(event) => setDraft({ ...draft, marks: event.target.value })}
                                style={{ maxWidth: 100 }}
                            />
                        </FormField>
                        <div className="question-card__editor-actions">
                            <Button variant="ghost" onClick={() => setEditing(false)}>Cancel</Button>
                            <Button variant="primary" onClick={save} loading={update.isPending}>
                                Save changes
                            </Button>
                        </div>
                    </div>
                ) : (
                    <>
                        <div className="question-card__question">{question.question}</div>
                        {question.options?.length ? (
                            <ol className="question-card__options">
                                {question.options.map((option) => (
                                    <li key={option}>{option}</li>
                                ))}
                            </ol>
                        ) : null}
                        {question.image && (
                            <div className="question-card__image">
                                <img src={question.image.startsWith("/") ? question.image : `/static/${question.image}`} alt="" />
                            </div>
                        )}
                        <details
                            open={expanded}
                            onToggle={(event) => setExpanded(event.target.open)}
                            className="question-card__answer"
                        >
                            <summary>Answer & metadata</summary>
                            <div className="question-card__answer-body">
                                <p><strong>Answer:</strong> {question.answer}</p>
                                <p>
                                    <strong>Learning outcomes:</strong>{" "}
                                    {(question.learningOutcomes || []).join(" · ") || "—"}
                                </p>
                                {question.images?.length ? (
                                    <div className="question-card__gallery">
                                        {question.images.map((image) => (
                                            <div key={image.imageId || image.url} className="question-card__gallery-item">
                                                <img src={image.url} alt={image.fileName || ""} />
                                                {image.imageId && (
                                                    <button
                                                        className="question-card__gallery-remove"
                                                        onClick={() => deleteImage.mutate(image.imageId)}
                                                        title="Remove image"
                                                    >
                                                        ×
                                                    </button>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                ) : null}
                            </div>
                        </details>
                    </>
                )}

                <div className="question-card__actions">
                    {editing ? null : (
                        <>
                            <Button variant="ghost" size="sm" onClick={startEdit}>Edit</Button>
                            <Button variant="ghost" size="sm" onClick={() => setRegenOpen(true)}>
                                Regenerate…
                            </Button>
                            <Button variant="ghost" size="sm" onClick={() => setAnswerRegenOpen(true)}>
                                Regenerate answer…
                            </Button>
                            <label className="question-card__upload">
                                <input
                                    type="file"
                                    accept="image/*"
                                    multiple
                                    onChange={(event) => {
                                        const files = Array.from(event.target.files || []);
                                        if (files.length) {
                                            upload.mutate({ questionId: question.questionId, files });
                                        }
                                        event.target.value = "";
                                    }}
                                />
                                Upload image
                            </label>
                            <Button variant="danger" size="sm" onClick={() => setConfirmDelete(true)}>
                                Delete
                            </Button>
                        </>
                    )}
                </div>
            </CardBody>

            <Modal
                open={regenOpen}
                title="Regenerate question"
                description="Rewrites the question, answer, and options."
                size="sm"
                onClose={() => setRegenOpen(false)}
                footer={
                    <>
                        <Button variant="ghost" onClick={() => setRegenOpen(false)}>Cancel</Button>
                        <Button
                            variant="primary"
                            loading={regenerate.isPending}
                            onClick={async () => {
                                await regenerate.mutateAsync({
                                    questionId: question.questionId,
                                    prompt: prompt.trim() || undefined,
                                });
                                setRegenOpen(false);
                                setPrompt("");
                            }}
                        >
                            Regenerate
                        </Button>
                    </>
                }
            >
                <FormField label="Prompt (optional)">
                    <Textarea
                        value={prompt}
                        onChange={(event) => setPrompt(event.target.value)}
                        placeholder="Make it more application-based."
                    />
                </FormField>
            </Modal>

            <Modal
                open={answerRegenOpen}
                title="Regenerate answer"
                description="Rewrites just the answer text."
                size="sm"
                onClose={() => setAnswerRegenOpen(false)}
                footer={
                    <>
                        <Button variant="ghost" onClick={() => setAnswerRegenOpen(false)}>Cancel</Button>
                        <Button
                            variant="primary"
                            loading={regenerateAnswer.isPending}
                            onClick={async () => {
                                await regenerateAnswer.mutateAsync({
                                    questionId: question.questionId,
                                    prompt: prompt.trim() || undefined,
                                });
                                setAnswerRegenOpen(false);
                                setPrompt("");
                            }}
                        >
                            Regenerate
                        </Button>
                    </>
                }
            >
                <FormField label="Prompt (optional)">
                    <Textarea
                        value={prompt}
                        onChange={(event) => setPrompt(event.target.value)}
                        placeholder="Give a more detailed answer."
                    />
                </FormField>
            </Modal>

            <ConfirmDialog
                open={confirmDelete}
                title="Delete question?"
                description="Historical submissions keep the locked snapshot of this question."
                tone="danger"
                confirmLabel="Delete"
                onCancel={() => setConfirmDelete(false)}
                onConfirm={async () => {
                    await remove.mutateAsync(question.questionId);
                    setConfirmDelete(false);
                }}
                loading={remove.isPending}
            />
        </Card>
    );
};

export default QuestionCard;
