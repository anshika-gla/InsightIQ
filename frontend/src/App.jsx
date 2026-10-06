import { useState } from "react";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const API_URL = "http://127.0.0.1:8000";

const CHART_COLORS = [
  "#4F46E5",
  "#7C3AED",
  "#06B6D4",
  "#10B981",
  "#F59E0B",
  "#EF4444",
  "#EC4899",
  "#8B5CF6",
];

/* =========================================================
   APP
   ========================================================= */

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /* =======================================================
     SUBMIT QUERY
     ======================================================= */

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!query.trim()) {
      setError("Please enter an analytics question.");
      return;
    }

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const result = await fetch(`${API_URL}/api/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query.trim(),
        }),
      });

      const data = await result.json();

      if (!result.ok) {
        throw new Error(
          data.detail || "Query processing failed."
        );
      }

      setResponse(data);
    } catch (err) {
      setError(
        err.message ||
          "Unable to connect to the InsightIQ backend."
      );
    } finally {
      setLoading(false);
    }
  };

  /* =======================================================
     FORMAT NUMBER
     ======================================================= */

  const formatNumber = (value) => {
    if (typeof value !== "number") {
      return value;
    }

    return Number(value.toFixed(2)).toLocaleString();
  };

  /* =======================================================
     GET CHART TYPE
     ======================================================= */

  const getChartType = () => {
    if (!response || !Array.isArray(response.result)) {
      return null;
    }

    const operation = response.logic?.operation;

    if (operation === "percentage") {
      return "pie";
    }

    if (
      operation === "rank" ||
      operation === "top_n"
    ) {
      return "bar";
    }

    if (operation === "time_analysis") {
      return "line";
    }

    return null;
  };

  /* =======================================================
     GET CHART DATA
     ======================================================= */

  const getChartData = () => {
    if (!Array.isArray(response?.result)) {
      return [];
    }

    return response.result;
  };

  /* =======================================================
     FIND NUMERIC COLUMN
     ======================================================= */

  const getNumericKey = () => {
    const rows = getChartData();

    if (!rows.length) {
      return null;
    }

    if (
      response?.logic?.operation === "percentage" &&
      "contribution_percentage" in rows[0]
    ) {
      return "contribution_percentage";
    }

    const ignoredKeys = [
      "year",
      "month",
      "_rank",
    ];

    return Object.keys(rows[0]).find(
      (key) =>
        typeof rows[0][key] === "number" &&
        !ignoredKeys.includes(key)
    );
  };

  /* =======================================================
     FIND CATEGORY / LABEL COLUMN
     ======================================================= */

  const getCategoryKey = () => {
    const rows = getChartData();

    if (!rows.length) {
      return null;
    }

    const preferredKeys = [
      "product_category",
      "category",
      "city",
      "region",
      "customer_id",
      "product_name",
      "year_month",
      "month",
    ];

    for (const key of preferredKeys) {
      if (
        key in rows[0] &&
        typeof rows[0][key] === "string"
      ) {
        return key;
      }
    }

    return Object.keys(rows[0]).find(
      (key) =>
        typeof rows[0][key] === "string"
    );
  };

  /* =======================================================
     PIE / DONUT CHART
     ======================================================= */

  const renderPieChart = () => {
    const data = getChartData();

    if (!data.length) {
      return null;
    }

    const categoryKey = getCategoryKey();

    if (!categoryKey) {
      return null;
    }

    const percentageKey =
      "contribution_percentage";

    if (!(percentageKey in data[0])) {
      return null;
    }

    return (
      <div className="chart-card">
        <div className="chart-heading">
          <h3>
            Sales Contribution by Category
          </h3>

          <p>
            Revenue contribution across product
            categories.
          </p>
        </div>

        <div className="chart-container">
          <ResponsiveContainer
            width="100%"
            height={380}
          >
            <PieChart>
              <Pie
                data={data}
                dataKey={percentageKey}
                nameKey={categoryKey}
                cx="50%"
                cy="50%"
                outerRadius={125}
                innerRadius={65}
                paddingAngle={3}
                label={({ name, value }) =>
                  `${name}: ${Number(
                    value
                  ).toFixed(1)}%`
                }
              >
                {data.map((_, index) => (
                  <Cell
                    key={`pie-cell-${index}`}
                    fill={
                      CHART_COLORS[
                        index %
                          CHART_COLORS.length
                      ]
                    }
                  />
                ))}
              </Pie>

              <Tooltip
                formatter={(value) =>
                  `${Number(value).toFixed(2)}%`
                }
              />

              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  /* =======================================================
     BAR CHART
     ======================================================= */

  const renderBarChart = () => {
    const data = getChartData();

    if (!data.length) {
      return null;
    }

    const categoryKey = getCategoryKey();
    const numericKey = getNumericKey();

    if (!categoryKey || !numericKey) {
      return null;
    }

    return (
      <div className="chart-card">
        <div className="chart-heading">
          <h3>
            Performance Ranking
          </h3>

          <p>
            Ranked comparison based on the
            selected metric.
          </p>
        </div>

        <div className="chart-container">
          <ResponsiveContainer
            width="100%"
            height={360}
          >
            <BarChart
              data={data}
              margin={{
                top: 10,
                right: 20,
                left: 0,
                bottom: 10,
              }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey={categoryKey}
              />

              <YAxis />

              <Tooltip />

              <Legend />

              <Bar
                dataKey={numericKey}
                name={numericKey.replaceAll(
                  "_",
                  " "
                )}
                radius={[
                  8,
                  8,
                  0,
                  0,
                ]}
              >
                {data.map((_, index) => (
                  <Cell
                    key={`bar-cell-${index}`}
                    fill={
                      CHART_COLORS[
                        index %
                          CHART_COLORS.length
                      ]
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  /* =======================================================
     LINE CHART
     ======================================================= */

  const renderLineChart = () => {
    const data = getChartData();

    if (!data.length) {
      return null;
    }

    const numericKey = getNumericKey();

    if (!numericKey) {
      return null;
    }

    const timeKey =
      data[0].year_month !== undefined
        ? "year_month"
        : getCategoryKey();

    if (!timeKey) {
      return null;
    }

    return (
      <div className="chart-card">
        <div className="chart-heading">
          <h3>
            Revenue Trend
          </h3>

          <p>
            Monthly analytics trend based on
            the selected metric.
          </p>
        </div>

        <div className="chart-container">
          <ResponsiveContainer
            width="100%"
            height={360}
          >
            <LineChart
              data={data}
              margin={{
                top: 10,
                right: 20,
                left: 0,
                bottom: 10,
              }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey={timeKey}
              />

              <YAxis />

              <Tooltip />

              <Legend />

              <Line
                type="monotone"
                dataKey={numericKey}
                name={numericKey.replaceAll(
                  "_",
                  " "
                )}
                stroke="#4F46E5"
                strokeWidth={3}
                dot={{
                  r: 5,
                  fill: "#4F46E5",
                }}
                activeDot={{
                  r: 7,
                }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  };

  /* =======================================================
     SELECT CHART
     ======================================================= */

  const renderChart = () => {
    const chartType = getChartType();

    if (!chartType) {
      return null;
    }

    if (chartType === "pie") {
      return renderPieChart();
    }

    if (chartType === "bar") {
      return renderBarChart();
    }

    if (chartType === "line") {
      return renderLineChart();
    }

    return null;
  };

  /* =======================================================
     RENDER RESULT
     ======================================================= */

  const renderResult = () => {
    if (!response?.result) {
      return null;
    }

    /* =====================================================
       ARRAY RESULT
       ===================================================== */

    if (Array.isArray(response.result)) {
      if (response.result.length === 0) {
        return (
          <p>
            No results found.
          </p>
        );
      }

      const columns = Object.keys(
        response.result[0]
      );

      return (
        <div className="result-table-wrapper">
          <table className="result-table">
            <thead>
              <tr>
                {columns.map((column) => (
                  <th key={column}>
                    {column.replaceAll(
                      "_",
                      " "
                    )}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              {response.result.map(
                (row, index) => (
                  <tr key={index}>
                    {columns.map((column) => (
                      <td key={column}>
                        {formatNumber(
                          row[column]
                        )}
                      </td>
                    ))}
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      );
    }

    /* =====================================================
       OBJECT RESULT
       ===================================================== */

    if (
      typeof response.result ===
      "object"
    ) {
      return (
        <div className="object-result">
          {Object.entries(
            response.result
          ).map(([key, value]) => (
            <div
              className="result-item"
              key={key}
            >
              <span>
                {key.replaceAll(
                  "_",
                  " "
                )}
              </span>

              <strong>
                {formatNumber(value)}
              </strong>
            </div>
          ))}
        </div>
      );
    }

    /* =====================================================
       SINGLE VALUE
       ===================================================== */

    return (
      <div className="single-result">
        {formatNumber(response.result)}
      </div>
    );
  };

  /* =========================================================
     UI
     ========================================================= */

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>InsightIQ</h1>

          <p>
            Intelligent Analytics Query Engine
          </p>
        </div>

        <div className="status-badge">
          ● Analytics Engine
        </div>
      </header>

      {/* MAIN */}
      <main className="container">

        {/* HERO */}
        <section className="hero">
          <h2>
            Ask your business data
          </h2>

          <p>
            Ask questions in natural language
            and get deterministic analytics
            results.
          </p>
        </section>

        {/* QUERY CARD */}
        <section className="query-card">
          <form onSubmit={handleSubmit}>

            <label htmlFor="query">
              Analytics Question
            </label>

            <textarea
              id="query"
              value={query}
              onChange={(event) =>
                setQuery(
                  event.target.value
                )
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

          {/* EXAMPLE QUERIES */}
          <div className="examples">

            <span>
              Try:
            </span>

            <button
              type="button"
              onClick={() =>
                setQuery(
                  "What are the total sales?"
                )
              }
            >
              Total Sales
            </button>

            <button
              type="button"
              onClick={() =>
                setQuery(
                  "What are the top 2 cities by profit?"
                )
              }
            >
              Top Cities
            </button>

            <button
              type="button"
              onClick={() =>
                setQuery(
                  "What is the sales contribution percentage by category?"
                )
              }
            >
              Contribution %
            </button>

            <button
              type="button"
              onClick={() =>
                setQuery(
                  "What are the top 3 customers in each region by revenue?"
                )
              }
            >
              Top Customers
            </button>

          </div>
        </section>

        {/* ERROR */}
        {error && (
          <section className="error-card">

            <strong>
              Query Error
            </strong>

            <p>
              {error}
            </p>

          </section>
        )}

        {/* RESULTS */}
        {response && (
          <section className="results-section">

            {/* RESULT HEADER */}
            <div className="result-header">

              <div>

                <span className="section-label">
                  RESULT
                </span>

                <h2>
                  {response.query}
                </h2>

              </div>

              {/* CONFIDENCE */}
              <div className="confidence">

                <span>
                  Confidence
                </span>

                <strong>
                  {Math.round(
                    response.confidence *
                      100
                  )}
                  %
                </strong>

              </div>

            </div>

            {/* ANSWER */}
            <div className="answer-card">

              <h3>
                Answer
              </h3>

              {renderResult()}

            </div>

            {/* CHART */}
            {renderChart()}

            {/* DETAILS */}
            <div className="details-grid">

              <div className="detail-card">

                <span>
                  Operation
                </span>

                <strong>
                  {response.logic
                    ?.operation || "-"}
                </strong>

              </div>

              <div className="detail-card">

                <span>
                  Metric
                </span>

                <strong>
                  {response.logic
                    ?.metric || "-"}
                </strong>

              </div>

              <div className="detail-card">

                <span>
                  Rows Returned
                </span>

                <strong>
                  {response.logic
                    ?.rows_returned ?? 0}
                </strong>

              </div>

            </div>

            {/* EXPLANATION */}
            <div className="explanation-card">

              <h3>
                Explanation
              </h3>

              <p>
                {response.explanation}
              </p>

            </div>

            {/* QUERY LOGIC */}
            <details className="logic-card">

              <summary>
                View Query Logic
              </summary>

              <pre>
                {JSON.stringify(
                  response.logic,
                  null,
                  2
                )}
              </pre>

            </details>

          </section>
        )}

      </main>
    </div>
  );
}

export default App;