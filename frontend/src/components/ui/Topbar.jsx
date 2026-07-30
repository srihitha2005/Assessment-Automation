import "./Topbar.css";

const Topbar = ({ breadcrumbs = [], right }) => (
    <header className="topbar">
        <nav className="topbar__breadcrumbs" aria-label="Breadcrumb">
            {breadcrumbs.map((item, index) => (
                <span key={index} className="topbar__crumb">
                    {item}
                    {index < breadcrumbs.length - 1 && <span className="topbar__separator">/</span>}
                </span>
            ))}
        </nav>
        <div className="topbar__right">{right}</div>
    </header>
);

export default Topbar;
