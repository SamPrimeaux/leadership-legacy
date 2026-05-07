export function DataTable({ columns, rows, getRowHref }) {
  return (
    <div className="dash-table" role="table">
      <div className="dash-table-head" role="row">
        {columns.map((column) => (
          <span key={column.key} role="columnheader">{column.label}</span>
        ))}
      </div>
      {rows.map((row) => {
        const content = columns.map((column) => (
          <span key={column.key} role="cell">
            {column.render ? column.render(row) : row[column.key]}
          </span>
        ));

        if (getRowHref) {
          return (
            <a className="dash-table-row" role="row" href={getRowHref(row)} key={row.id}>
              {content}
            </a>
          );
        }

        return (
          <div className="dash-table-row" role="row" key={row.id}>
            {content}
          </div>
        );
      })}
    </div>
  );
}
