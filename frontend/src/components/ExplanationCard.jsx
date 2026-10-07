function ExplanationCard({ explanation }) {
  return (
    <div className="explanation-card">
      <h3>Explanation</h3>

      <p>
        {explanation ||
          "No explanation available."}
      </p>
    </div>
  );
}

export default ExplanationCard;