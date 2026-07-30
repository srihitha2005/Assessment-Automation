import Badge from "../components/ui/Badge.jsx";
import Card, { CardBody, CardHeader } from "../components/ui/Card.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import PageHeader from "../components/ui/PageHeader.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import { usePropagationEvents } from "../hooks/usePropagation.js";
import { formatDateTime } from "../lib/format.js";
import "./PropagationEvents.css";

const PropagationEvents = () => {
    const { data, isLoading, isError, error } = usePropagationEvents();

    if (isLoading) return <Spinner label="Loading propagation events…" size="lg" />;
    if (isError) return <EmptyState icon="!" title="Could not load events" description={error.message} />;

    if (!data.length)
        return (
            <>
                <PageHeader
                    eyebrow="Propagation"
                    title="Dynamic outcome propagation"
                    description="Simulate a planner edit from any planner page — this feed will show the diff and which assessments were marked Outdated."
                />
                <EmptyState
                    icon="↻"
                    title="No planner changes yet"
                    description="Open a planner and use “Edit outcomes (simulate)” to record one."
                />
            </>
        );

    return (
        <>
            <PageHeader
                eyebrow="Propagation"
                title="Dynamic outcome propagation"
                description="Every time a planner's learning outcomes change, we record the diff, mark impacted assessments as Outdated, and let teachers regenerate on their own timeline."
            />

            <div className="propagation__grid">
                {data.map((event) => (
                    <Card key={event.eventId} padding="none">
                        <CardHeader>
                            <div>
                                <div className="propagation__title">Planner {event.plannerId}</div>
                                <div className="propagation__meta">
                                    {formatDateTime(event.createdOn)} · triggered by {event.triggeredBy}
                                </div>
                            </div>
                            <Badge tone={event.resolution === "Pending" ? "warning" : "neutral"}>
                                {event.resolution}
                            </Badge>
                        </CardHeader>
                        <CardBody>
                            <div className="propagation__section">
                                <div className="propagation__label">Added</div>
                                {event.addedOutcomes.length ? (
                                    <ul className="propagation__outcomes propagation__outcomes--added">
                                        {event.addedOutcomes.map((outcome) => (
                                            <li key={outcome}>+ {outcome}</li>
                                        ))}
                                    </ul>
                                ) : (
                                    <span className="propagation__empty">None</span>
                                )}
                            </div>
                            <div className="propagation__section">
                                <div className="propagation__label">Removed</div>
                                {event.removedOutcomes.length ? (
                                    <ul className="propagation__outcomes propagation__outcomes--removed">
                                        {event.removedOutcomes.map((outcome) => (
                                            <li key={outcome}>− {outcome}</li>
                                        ))}
                                    </ul>
                                ) : (
                                    <span className="propagation__empty">None</span>
                                )}
                            </div>
                            <div className="propagation__section">
                                <div className="propagation__label">Affected assessments</div>
                                {event.affectedAssessmentIds.length ? (
                                    <div className="propagation__ids">
                                        {event.affectedAssessmentIds.map((id) => (
                                            <a key={id} href={`/assessments/${id}`}>
                                                {id.slice(0, 8)}…
                                            </a>
                                        ))}
                                    </div>
                                ) : (
                                    <span className="propagation__empty">None</span>
                                )}
                            </div>
                        </CardBody>
                    </Card>
                ))}
            </div>
        </>
    );
};

export default PropagationEvents;
