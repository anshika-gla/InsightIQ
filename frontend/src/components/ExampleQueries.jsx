function ExampleQueries({ setQuery }) {
  const examples = [
    {
      label: "Total Sales",
      query: "What are the total sales?",
    },
    {
      label: "Top Cities",
      query: "What are the top 2 cities by profit?",
    },
    {
      label: "Contribution %",
      query:
        "What is the sales contribution percentage by category?",
    },
    {
      label: "Top Customers",
      query:
        "What are the top 3 customers in each region by revenue?",
    },
  ];

  return (
    <div className="examples">
      <span>Try:</span>

      {examples.map((example) => (
        <button
          key={example.label}
          type="button"
          onClick={() => setQuery(example.query)}
        >
          {example.label}
        </button>
      ))}
    </div>
  );
}

export default ExampleQueries;