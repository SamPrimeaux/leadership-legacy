export function StatusBadge({ status }) {
  return <span className={`status-badge status-${String(status).replaceAll(" ", "-")}`}>{status}</span>;
}
