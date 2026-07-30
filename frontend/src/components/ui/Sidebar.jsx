import { NavLink } from "react-router-dom";

import { NAV_ITEMS } from "../../lib/constants.js";
import "./Sidebar.css";

const Sidebar = () => (
    <aside className="sidebar">
        <div className="sidebar__brand">
            <span className="sidebar__mark">AA</span>
            <div className="sidebar__brand-text">
                <div className="sidebar__brand-title">Assessment</div>
                <div className="sidebar__brand-subtitle">Automation Pipeline</div>
            </div>
        </div>
        <nav className="sidebar__nav">
            {NAV_ITEMS.map((item) => (
                <NavLink
                    key={item.to}
                    to={item.to}
                    end={item.to === "/"}
                    className={({ isActive }) =>
                        `sidebar__link${isActive ? " sidebar__link--active" : ""}`
                    }
                >
                    <span className="sidebar__icon" aria-hidden>
                        {item.icon}
                    </span>
                    {item.label}
                </NavLink>
            ))}
        </nav>
        <div className="sidebar__footer">
            <span className="sidebar__version">v2.0 &middot; Ollama · qwen2.5:3b</span>
        </div>
    </aside>
);

export default Sidebar;
