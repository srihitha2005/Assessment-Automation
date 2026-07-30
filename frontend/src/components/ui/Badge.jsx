import "./Badge.css";

const Badge = ({ tone = "neutral", children, className = "", icon }) => (
    <span className={["badge", `badge--${tone}`, className].filter(Boolean).join(" ")}>
        {icon && <span className="badge__icon">{icon}</span>}
        {children}
    </span>
);

export default Badge;
