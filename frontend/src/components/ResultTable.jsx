function ResultTable({ result }) {
  if (!Array.isArray(result)) {
    return null;
  }

  if (result.length === 0) {
    return <p>No results found.</p>;
  }

  const columns = Object.keys(result[0]);

  const formatValue = (value) => {
    if (typeof value === "number") {
      return Number(value.toFixed(2)).toLocaleString();
    }

    return value;
  };

  return (
    <div className="result-table-wrapper">
      <table className="result-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>
                {column.replaceAll("_", " ")}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {result.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column}>
                  {formatValue(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ResultTable;