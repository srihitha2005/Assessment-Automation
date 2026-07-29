import "./Button.css";

function Button({text, onClick, disabled = false}){
    return (
        <button className = "button" onClick = {onClick} disabled = {disabled}>
            {text}
        </button>
    );
}
export default Button;