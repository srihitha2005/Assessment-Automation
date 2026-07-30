import "./StatTile.css";

const StatTile = ({ label, value, hint, tone = "brand", icon }) => (
    <div className={`stat-tile stat-tile--${tone}`}>
        <div className="stat-tile__label">
            {icon && <span className="stat-tile__icon" aria-hidden>{icon}</span>}
            {label}
        </div>
        <div className="stat-tile__value">{value}</div>
        {hint && <div className="stat-tile__hint">{hint}</div>}
    </div>
);

export default StatTile;
