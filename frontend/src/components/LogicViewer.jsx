function LogicViewer({ logic }) {
  if (!logic) {
    return null;
  }

  return (
    <details className="logic-card">
      <summary>
        View Query Logic
      </summary>

      <pre>
        {JSON.stringify(
          logic,
          null,
          2
        )}
      </pre>
    </details>
  );
}

export default LogicViewer;