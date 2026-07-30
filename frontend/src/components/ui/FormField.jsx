import "./FormField.css";

export const FormField = ({ label, hint, error, children, htmlFor }) => (
    <label className="form-field" htmlFor={htmlFor}>
        {label && <span className="form-field__label">{label}</span>}
        {children}
        {(hint || error) && (
            <span className={`form-field__hint ${error ? "form-field__hint--error" : ""}`}>
                {error || hint}
            </span>
        )}
    </label>
);

export const TextInput = ({ className = "", ...rest }) => (
    <input className={`form-input ${className}`} {...rest} />
);

export const Textarea = ({ className = "", rows = 4, ...rest }) => (
    <textarea className={`form-input form-input--textarea ${className}`} rows={rows} {...rest} />
);

export const Select = ({ className = "", children, ...rest }) => (
    <select className={`form-input form-input--select ${className}`} {...rest}>
        {children}
    </select>
);

export default FormField;
