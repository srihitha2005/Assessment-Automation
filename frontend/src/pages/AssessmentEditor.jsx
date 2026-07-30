import { useParams } from "react-router-dom";

import AssessmentToolbar from "../components/assessment/AssessmentToolbar.jsx";
import SubmissionPanel from "../components/assessment/SubmissionPanel.jsx";
import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import QuestionCard from "../components/question/QuestionCard.jsx";
import { useAssessment, useAssessmentQuestions } from "../hooks/useAssessments.js";
import "./AssessmentEditor.css";

const AssessmentEditor = () => {
    const { assessmentId } = useParams();
    const assessment = useAssessment(assessmentId);
    const questions = useAssessmentQuestions(assessmentId);

    if (assessment.isLoading) return <Spinner label="Loading assessment…" size="lg" />;
    if (assessment.isError || !assessment.data) {
        return (
            <EmptyState
                icon="!"
                title="Assessment not found"
                description={assessment.error?.message || "It may have been deleted."}
            />
        );
    }

    return (
        <>
            <AssessmentToolbar assessment={assessment.data} />

            <Card padding="none" className="assessment-editor__outcomes">
                <CardHeader>
                    <div>
                        <div className="assessment-editor__section-title">Learning outcomes</div>
                        <div className="assessment-editor__section-hint">
                            Coverage across the assessment. Any gaps are surfaced in the toolbar warning above.
                        </div>
                    </div>
                </CardHeader>
                <CardBody>
                    <ul className="assessment-editor__outcome-list">
                        {(assessment.data.learningOutcomes || []).map((outcome, index) => (
                            <li key={outcome}>
                                <span className="assessment-editor__outcome-index">{index + 1}</span>
                                {outcome}
                            </li>
                        ))}
                    </ul>
                </CardBody>
            </Card>

            <section className="assessment-editor__questions">
                <div className="assessment-editor__questions-header">
                    <h2>Questions</h2>
                    <span className="assessment-editor__questions-count">
                        {questions.data?.length || 0} question(s)
                    </span>
                </div>
                {questions.isLoading ? (
                    <Spinner label="Loading questions…" />
                ) : questions.isError ? (
                    <EmptyState icon="!" title="Could not load questions" description={questions.error.message} />
                ) : questions.data?.length ? (
                    <div className="assessment-editor__question-grid">
                        {questions.data.map((question) => (
                            <QuestionCard
                                key={question.questionId}
                                assessmentId={assessmentId}
                                question={question}
                            />
                        ))}
                    </div>
                ) : (
                    <EmptyState
                        icon="?"
                        title="No questions yet"
                        description="Try regenerating to fill this assessment."
                    />
                )}
            </section>

            <section className="assessment-editor__submissions">
                <SubmissionPanel assessmentId={assessmentId} questions={questions.data || []} />
            </section>
        </>
    );
};

export default AssessmentEditor;
