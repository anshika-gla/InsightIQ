function QueryInput({
  query,
  setQuery,
  onSubmit,
  loading,
}) {
  return (
    <section className="query-card">
      <form onSubmit={onSubmit}>
        <label htmlFor="query">
          Analytics Question
        </label>

        <textarea
          id="query"
          value={query}
          onChange={(event) =>
            setQuery(event.target.value)
          }
          placeholder="Example: What are the top 2 cities by profit?"
          rows={4}
        />

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Query"}
        </button>
      </form>
    </section>
  );
}

export default QueryInput;