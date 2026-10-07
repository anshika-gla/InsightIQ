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

import Header from "./components/Header";
import QueryInput from "./components/QueryInput";
import ExampleQueries from "./components/ExampleQueries";
import ResultTable from "./components/ResultTable";
import ConfidenceCard from "./components/ConfidenceCard";
import ExplanationCard from "./components/ExplanationCard";
import UnderstandingCard from "./components/UnderstandingCard";
import LogicViewer from "./components/LogicViewer";
import LoadingState from "./components/LoadingState";
import ErrorMessage from "./components/ErrorMessage";

import { analyzeQuery } from "./services/api";

import {
  formatNumber,
  formatColumnName,
} from "./utils/formatters";

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

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // --------------------------------
  // SUBMIT QUERY
  // --------------------------------

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
      const data = await analyzeQuery(query);

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

  // --------------------------------
  // CHART TYPE
  // --------------------------------

  const getChartType = () => {
    if (!response || !Array.isArray(response.result)) {
      return null;
    }

    const operation =
      response.generated_logic?.operation;

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

  // --------------------------------
  // CHART DATA
  // --------------------------------

  const getChartData = () => {
    if (!Array.isArray(response?.result)) {
      return [];
    }

    return response.result;
  };

  // --------------------------------
  // NUMERIC KEY
  // --------------------------------

  const getNumericKey = () => {
    const rows = getChartData();

    if (!rows.length) {
      return null;
    }

    if (
      response?.generated_logic?.operation ===
        "percentage" &&
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

  // --------------------------------
  // CATEGORY KEY
  // --------------------------------

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

  // --------------------------------
  // PIE CHART
  // --------------------------------

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
                  `${name}: ${Number(value).toFixed(
                    1
                  )}%`
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

  // --------------------------------
  // BAR CHART
  // --------------------------------

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
          <h3>Performance Ranking</h3>

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
                name={formatColumnName(
                  numericKey
                )}
                radius={[8, 8, 0, 0]}
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

  // --------------------------------
  // LINE CHART
  // --------------------------------

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
          <h3>Revenue Trend</h3>

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

              <XAxis dataKey={timeKey} />

              <YAxis />

              <Tooltip />

              <Legend />

              <Line
                type="monotone"
                dataKey={numericKey}
                name={formatColumnName(
                  numericKey
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

  // --------------------------------
  // RENDER CHART
  // --------------------------------

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

  // --------------------------------
  // MAIN UI
  // --------------------------------

  return (
    <div className="app">

      <Header />

      <main className="container">

        {/* HERO */}
        <section className="hero">
          <h2>Ask your business data</h2>

          <p>
            Ask questions in natural language
            and get deterministic analytics
            results.
          </p>
        </section>

        {/* QUERY INPUT */}
        <QueryInput
          query={query}
          setQuery={setQuery}
          onSubmit={handleSubmit}
          loading={loading}
        />

        {/* EXAMPLES */}
        <ExampleQueries
          setQuery={setQuery}
        />

        {/* LOADING */}
        {loading && <LoadingState />}

        {/* ERROR */}
        <ErrorMessage message={error} />

        {/* RESULTS */}
        {response && !loading && (
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

              <ConfidenceCard
                confidence={
                  response.confidence_score
                }
              />

            </div>

            {/* ANSWER */}
            <div className="answer-card">
              <h3>Answer</h3>

              {Array.isArray(
                response.result
              ) ? (
                <ResultTable
                  result={response.result}
                />
              ) : typeof response.result ===
                  "object" &&
                response.result !== null ? (
                <div className="object-result">

                  {Object.entries(
                    response.result
                  ).map(([key, value]) => (
                    <div
                      className="result-item"
                      key={key}
                    >
                      <span>
                        {formatColumnName(key)}
                      </span>

                      <strong>
                        {typeof value ===
                        "number"
                          ? formatNumber(value)
                          : value}
                      </strong>
                    </div>
                  ))}

                </div>
              ) : (
                <div className="single-result">

                  {typeof response.result ===
                  "number"
                    ? formatNumber(
                        response.result
                      )
                    : response.result}

                </div>
              )}
            </div>

            {/* CHART */}
            {renderChart()}

            {/* UNDERSTANDING */}
            <UnderstandingCard
              logic={
                response.generated_logic
              }
            />

            {/* EXPLANATION */}
            <ExplanationCard
              explanation={
                response.explanation
              }
            />

            {/* LOGIC */}
            <LogicViewer
              logic={
                response.generated_logic
              }
            />

          </section>
        )}

      </main>
    </div>
  );
}

export default App;