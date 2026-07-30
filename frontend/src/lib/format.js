export const formatDateTime = (iso) => {
    if (!iso) return "—";
    const date = new Date(iso);
    if (Number.isNaN(date.getTime())) return "—";
    return date.toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
};

export const formatVersion = (version) => (version ? `v${version}` : "—");

export const truncate = (value, length = 120) => {
    if (!value) return "";
    return value.length > length ? `${value.slice(0, length - 1)}…` : value;
};

export const pluralise = (count, singular, plural) =>
    `${count} ${count === 1 ? singular : plural || `${singular}s`}`;
