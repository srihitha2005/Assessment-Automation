import "./Card.css";

const Card = ({ children, className = "", padding = "md", as: Tag = "div", ...rest }) => (
    <Tag className={["card", `card--pad-${padding}`, className].filter(Boolean).join(" ")} {...rest}>
        {children}
    </Tag>
);

export const CardHeader = ({ children, className = "" }) => (
    <div className={["card__header", className].filter(Boolean).join(" ")}>{children}</div>
);

export const CardBody = ({ children, className = "" }) => (
    <div className={["card__body", className].filter(Boolean).join(" ")}>{children}</div>
);

export const CardFooter = ({ children, className = "" }) => (
    <div className={["card__footer", className].filter(Boolean).join(" ")}>{children}</div>
);

export default Card;
