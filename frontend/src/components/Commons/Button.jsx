import "./styles/Button.css";

function Button({ text, onClick, disabled = false }) {
    const handleClick = (event) => {
        console.log("[Button] Clicked:", text);
        if (onClick) {
            onClick(event);
        }
    };

    return (
        <button
            className="button"
            onClick={handleClick}
            disabled={disabled}
            type="button"
        >
            {text}
        </button>
    );
}

export default Button;
