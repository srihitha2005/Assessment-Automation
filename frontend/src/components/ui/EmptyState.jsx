import "./EmptyState.css";

const EmptyState = ({ icon = "◍", title, description, action }) => (
    <div className="empty-state">
        <div className="empty-state__icon" aria-hidden>
            {icon}
        </div>
        <h3 className="empty-state__title">{title}</h3>
        {description && <p className="empty-state__description">{description}</p>}
        {action && <div className="empty-state__action">{action}</div>}
    </div>
);

export default EmptyState;
