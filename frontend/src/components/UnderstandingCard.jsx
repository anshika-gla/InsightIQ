function UnderstandingCard({ logic }) {
  if (!logic) {
    return null;
  }

  return (
    <div className="details-grid">
      <div className="detail-card">
        <span>Operation</span>

        <strong>
          {logic.operation || "-"}
        </strong>
      </div>

      <div className="detail-card">
        <span>Metric</span>

        <strong>
          {logic.metric || "-"}
        </strong>
      </div>

      <div className="detail-card">
        <span>Rows Returned</span>

        <strong>
          {logic.rows_returned ?? 0}
        </strong>
      </div>
    </div>
  );
}

export default UnderstandingCard;