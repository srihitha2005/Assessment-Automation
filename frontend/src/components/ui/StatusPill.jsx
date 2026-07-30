import Badge from "./Badge.jsx";
import { STATUS_TOKENS } from "../../lib/constants.js";

const StatusPill = ({ status }) => {
    const token = STATUS_TOKENS[status] || { label: status || "Unknown", color: "neutral" };
    return <Badge tone={token.color}>{token.label}</Badge>;
};

export default StatusPill;
