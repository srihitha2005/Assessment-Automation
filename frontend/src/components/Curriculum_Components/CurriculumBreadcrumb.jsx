import { Breadcrumbs, Link, Typography } from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import "./styles/CurriculumBreadcrumb.css";

function CurriculumBreadcrumb({ items = [] }) {
    return (
        <div className="curriculum-breadcrumb">
            <Breadcrumbs aria-label="curriculum breadcrumb">
                {
                    items.map((item, index) => {
                        const isLast = index === items.length - 1;

                        if (isLast || !item.to) {
                            return (
                                <Typography key={item.label} color="text.primary">
                                    {item.label}
                                </Typography>
                            );
                        }

                        return (
                            <Link
                                key={item.label}
                                component={RouterLink}
                                to={item.to}
                                underline="hover"
                                color="inherit"
                                onClick={() => console.log("[CurriculumBreadcrumb] Navigate:", item.to)}
                            >
                                {item.label}
                            </Link>
                        );
                    })
                }
            </Breadcrumbs>
        </div>
    );
}

export default CurriculumBreadcrumb;
