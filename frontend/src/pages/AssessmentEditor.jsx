import "./AssessmentEditor.css";

import { useParams } from "react-router-dom";

import AssessmentHeader from "../components/AssessmentHeader.jsx";
import QuestionCard from "../components/QuestionCard.jsx";

import useAssessmentByID from "../hooks/useAssessmentByID.js";
import useGetAllQuestions from "../hooks/useGetAllQuestions.js";

const AssessmentEditor = () => {
    // alert("AssessmentEditor loaded");

    const { assessmentId, assessmentID } = useParams();
    const id = assessmentId || assessmentID;

    console.log("[AssessmentEditor] Assessment ID:", id);

    const {

        assessment,
        loading: loadingAssessment,
        error: errorAssessment

    } = useAssessmentByID(id);

    const {

        questions,
        loading: loadingQuestions,
        error: errorQuestions

    } = useGetAllQuestions(id);

    if (loadingAssessment) {

        return (

            <div className="assessment-editor-message">

                Loading Assessment...

            </div>

        );

    }

    if (errorAssessment) {

        return (

            <div className="assessment-editor-message error">

                {errorAssessment}

            </div>

        );

    }

    return (

        <div className="assessment-editor">

            <AssessmentHeader
                assessment={assessment}
            />

            {

                loadingQuestions ?

                    (

                        <div className="assessment-editor-message">

                            Loading Questions...

                        </div>

                    )

                    :

                    errorQuestions ?

                        (

                            <div className="assessment-editor-message error">

                                {errorQuestions}

                            </div>

                        )

                        :

                        (

                            <div className="question-grid">

                                {

                                    questions.map((question) => (

                                        <QuestionCard

                                            key={question.questionId}

                                            question={question}

                                        />

                                    ))

                                }

                            </div>

                        )

            }

        </div>

    );

};

export default AssessmentEditor;
