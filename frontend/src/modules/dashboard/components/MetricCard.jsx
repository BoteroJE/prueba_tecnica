export function MetricCard({
  label,
  value,
  description,
  variant = "default",
}) {
  return (
    <article className={`metric-card metric-card-${variant}`}>
      <span className="metric-card-label">
        {label}
      </span>

      <strong className="metric-card-value">
        {value}
      </strong>

      <p className="metric-card-description">
        {description}
      </p>
    </article>
  );
}