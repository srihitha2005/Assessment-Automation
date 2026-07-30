import "./Spinner.css";

const Spinner = ({ label = "Loading…", size = "md" }) => (
    <div className={`spinner spinner--${size}`} role="status" aria-live="polite">
        <span className="spinner__ring" aria-hidden />
        <span className="spinner__label">{label}</span>
    </div>
);

export default Spinner;
