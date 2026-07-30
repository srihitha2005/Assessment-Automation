import { Link } from "react-router-dom";

import Button from "../components/ui/Button.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";

const NotFound = () => (
    <EmptyState
        icon="?"
        title="Page not found"
        description="The route you tried does not exist."
        action={
            <Link to="/">
                <Button variant="primary">Back to dashboard</Button>
            </Link>
        }
    />
);

export default NotFound;
