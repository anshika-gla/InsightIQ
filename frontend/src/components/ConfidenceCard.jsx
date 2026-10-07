function ConfidenceCard({ confidence }) {
  const percentage = Math.round(
    (confidence ?? 0) * 100
  );

  return (
    <div className="confidence">
      <span>Confidence</span>

      <strong>{percentage}%</strong>
    </div>
  );
}

export default ConfidenceCard;