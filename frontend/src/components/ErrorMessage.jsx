function ErrorMessage({ message }) {
  if (!message) {
    return null;
  }

  return (
    <section className="error-card">
      <strong>Query Error</strong>

      <p>{message}</p>
    </section>
  );
}

export default ErrorMessage;