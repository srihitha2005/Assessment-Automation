import { Link, Outlet, useLocation } from "react-router-dom";

import Sidebar from "./components/ui/Sidebar.jsx";
import Topbar from "./components/ui/Topbar.jsx";
import "./AppShell.css";

const CRUMB_MAP = [
    { pattern: /^\/$/, crumbs: () => ["Dashboard"] },
    { pattern: /^\/curriculum/, crumbs: () => ["Curriculum"] },
    { pattern: /^\/planners$/, crumbs: () => ["Planners"] },
    { pattern: /^\/planners\/(?<id>[^/]+)$/, crumbs: (match) => ["Planners", match.groups.id] },
    { pattern: /^\/assessments$/, crumbs: () => ["Assessments"] },
    {
        pattern: /^\/assessments\/(?<id>[^/]+)\/versions$/,
        crumbs: (match) => [
            <Link key="1" to="/assessments">Assessments</Link>,
            <Link key="2" to={`/assessments/${match.groups.id}`}>{match.groups.id.slice(0, 8)}…</Link>,
            "Versions",
        ],
    },
    {
        pattern: /^\/assessments\/(?<id>[^/]+)\/publish$/,
        crumbs: (match) => [
            <Link key="1" to="/assessments">Assessments</Link>,
            <Link key="2" to={`/assessments/${match.groups.id}`}>{match.groups.id.slice(0, 8)}…</Link>,
            "Publish",
        ],
    },
    {
        pattern: /^\/assessments\/(?<id>[^/]+)$/,
        crumbs: (match) => [
            <Link key="1" to="/assessments">Assessments</Link>,
            `${match.groups.id.slice(0, 8)}…`,
        ],
    },
    { pattern: /^\/question-bank/, crumbs: () => ["Question Bank"] },
    { pattern: /^\/propagation/, crumbs: () => ["Propagation"] },
];

const buildCrumbs = (pathname) => {
    for (const rule of CRUMB_MAP) {
        const match = pathname.match(rule.pattern);
        if (match) return rule.crumbs(match);
    }
    return ["Page"];
};

const AppShell = () => {
    const location = useLocation();
    const crumbs = buildCrumbs(location.pathname);
    return (
        <div className="shell">
            <Sidebar />
            <div className="shell__main">
                <Topbar breadcrumbs={crumbs} right={<span className="shell__env">Local · SQLite</span>} />
                <main className="shell__content">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default AppShell;
