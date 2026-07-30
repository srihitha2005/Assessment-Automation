import "./Button.css";

const Button = ({
    variant = "primary",
    size = "md",
    type = "button",
    icon,
    loading = false,
    disabled = false,
    onClick,
    children,
    className = "",
    ...rest
}) => {
    const classes = ["btn", `btn--${variant}`, `btn--${size}`, className].filter(Boolean).join(" ");
    return (
        <button
            type={type}
            className={classes}
            onClick={onClick}
            disabled={disabled || loading}
            {...rest}
        >
            {loading ? <span className="btn__spinner" aria-hidden /> : icon ? <span className="btn__icon">{icon}</span> : null}
            <span>{children}</span>
        </button>
    );
};

export default Button;
