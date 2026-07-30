import "./Table.css";

const Table = ({ columns, rows, emptyLabel = "No records yet.", getRowKey }) => {
    if (!rows.length) {
        return <div className="table-empty">{emptyLabel}</div>;
    }
    return (
        <div className="table-wrapper">
            <table className="table">
                <thead>
                    <tr>
                        {columns.map((column) => (
                            <th key={column.key} style={{ width: column.width }}>
                                {column.header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {rows.map((row, index) => (
                        <tr key={getRowKey ? getRowKey(row, index) : index}>
                            {columns.map((column) => (
                                <td key={column.key}>{column.render ? column.render(row) : row[column.key]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Table;
