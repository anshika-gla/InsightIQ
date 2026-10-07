# InsightIQ — Intelligent Analytics Query Engine

InsightIQ is a GenAI-powered analytics query engine that converts natural-language business questions into executable analytical logic and returns structured, explainable results.

## Features

- Natural-language analytics queries
- GenAI-based query understanding
- Structured query-plan generation
- Query-plan validation
- Deterministic analytics execution using Pandas
- Sum, average and count aggregations
- Grouping and filtering
- Ranking and Top-N queries
- Top-N within groups
- Contribution percentage analysis
- Average Order Value (AOV)
- Target vs actual comparison
- Monthly analysis
- Year-over-Year analysis
- Confidence scoring
- Human-readable explanations
- Unsupported-query handling
- Local fallback planner
- FastAPI REST API
- React frontend
- Recharts visualizations
- Automated backend tests

---

## Architecture

    User Query
        |
        v
    React Frontend
        |
        v
    FastAPI Backend
        |
        v
    Query Service
        |
        +----------------------+
        |                      |
        v                      v
    GenAI Planner        Local Fallback
        |                      |
        +----------+-----------+
                   |
                   v
          Query Plan Validation
                   |
                   v
          Analytics Executor
                   |
          +--------+--------+
          |        |        |
          v        v        v
      Aggregation Ranking Comparison
          |        |        |
          +--------+--------+
                   |
                   v
          Confidence Scoring
                   |
                   v
          Explanation Generation
                   |
                   v
            Structured Response
                   |
                   v
             React Frontend

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Pandas
- Uvicorn

### AI

- Google Gemini API
- Local fallback planner

### Frontend

- React
- Vite
- JavaScript
- Recharts

### Testing

- Pytest

### Data

- CSV
- JSON

---

## Project Structure

    InsightIQ/
    |
    +-- backend/
    |   +-- main.py
    |   +-- requirements.txt
    |   +-- .env
    |   |
    |   +-- ai/
    |   |   +-- client.py
    |   |   +-- prompts.py
    |   |   +-- schemas.py
    |   |
    |   +-- api/
    |   |   +-- routes.py
    |   |
    |   +-- data/
    |   |   +-- loader.py
    |   |   +-- dictionary.py
    |   |
    |   +-- dataset/
    |   |   +-- sales_data.csv
    |   |   +-- targets.csv
    |   |   +-- data_dictionary.json
    |   |   +-- nl_queries.json
    |   |
    |   +-- engine/
    |   |   +-- aggregations.py
    |   |   +-- comparisons.py
    |   |   +-- executor.py
    |   |   +-- filters.py
    |   |   +-- nested_queries.py
    |   |   +-- percentages.py
    |   |   +-- ranking.py
    |   |   +-- time_analysis.py
    |   |   +-- validator.py
    |   |
    |   +-- models/
    |   |   +-- query_models.py
    |   |
    |   +-- services/
    |   |   +-- confidence_service.py
    |   |   +-- explanation_service.py
    |   |   +-- query_service.py
    |   |
    |   +-- tests/
    |       +-- test_executor.py
    |
    +-- frontend/
    |   +-- package.json
    |   +-- vite.config.js
    |   +-- index.html
    |   |
    |   +-- src/
    |       +-- main.jsx
    |       +-- App.jsx
    |       +-- App.css
    |       |
    |       +-- components/
    |       |   +-- Header.jsx
    |       |   +-- QueryInput.jsx
    |       |   +-- ExampleQueries.jsx
    |       |   +-- ResultTable.jsx
    |       |   +-- ConfidenceCard.jsx
    |       |   +-- ExplanationCard.jsx
    |       |   +-- UnderstandingCard.jsx
    |       |   +-- LogicViewer.jsx
    |       |   +-- LoadingState.jsx
    |       |   +-- ErrorMessage.jsx
    |       |
    |       +-- services/
    |       |   +-- api.js
    |       |
    |       +-- utils/
    |           +-- formatters.js
    |
    +-- sample_outputs/
    |   +-- query_01.json
    |   +-- query_02.json
    |   +-- query_03.json
    |   +-- query_04.json
    |   +-- query_05.json
    |
    +-- README.md
    +-- LICENSE
    +-- .gitignore

---

## Dataset

The project uses the following files:

### sales_data.csv

Contains sales transaction data including:

- Order ID
- Order Date
- Region
- Country
- City
- Customer ID
- Customer Segment
- Product Category
- Product Subcategory
- Product Name
- Quantity
- Unit Price
- Discount
- Shipping Cost
- Profit

### targets.csv

Contains regional monthly revenue targets.

### data_dictionary.json

Contains information about dataset fields and their meaning.

### nl_queries.json

Contains example natural-language analytics queries.

---

## Query Processing

InsightIQ processes every query through the following pipeline:

    Natural Language Query
            |
            v
    GenAI / Local Planner
            |
            v
    Structured Query Plan
            |
            v
    Query Validation
            |
            v
    Deterministic Execution
            |
            v
    Confidence Score
            |
            v
    Explanation
            |
            v
    Final Result

### Example

User query:

    What are the top 2 cities by profit?

Generated query plan:

    {
      "operation": "top_n",
      "metric": "profit",
      "group_by": ["city"],
      "limit": 2,
      "order": "desc"
    }

The query plan is validated and then executed by the analytics engine.

---

## Supported Analytics

### Aggregations

- Sum
- Average
- Count

### Grouping

The system can group analytical results by supported dataset fields such as:

- Region
- City
- Product Category
- Customer
- Product

### Filtering

Queries can filter data using supported conditions.

### Ranking

The system supports:

- Top-N
- Ranking by metric
- Ranking within groups

### Contribution Percentage

The system calculates each group's contribution to the total metric.

### Average Order Value

AOV is calculated as:

    Total Revenue / Number of Unique Orders

### Target Comparison

The system compares actual revenue with target revenue and returns:

- Actual revenue
- Target revenue
- Difference
- Achievement percentage
- Target status

### Time Analysis

The system supports:

- Monthly analysis
- Year-over-Year analysis

If sufficient historical data is not available, the system returns an insufficient-data response instead of generating a false percentage.

---

## Example Queries

### 1. Total Sales

Query:

    What are the total sales?

Result:

    6134.4

Generated logic:

    Operation: sum
    Metric: revenue
    Aggregation: sum

---

### 2. Top 2 Cities by Profit

Query:

    What are the top 2 cities by profit?

Result:

    New York        200
    San Francisco   180

The engine groups transactions by city, calculates total profit, sorts the results and returns the top two cities.

---

### 3. Average Order Value by Region

Query:

    What is the average order value by region?

Result:

    APAC    118.50
    EMEA    799.33
    NA      1087.47

AOV is calculated using total revenue divided by the number of unique orders.

---

### 4. Revenue Contribution by Category

Query:

    What percentage of revenue comes from each category?

Result:

    Technology        88.06%
    Furniture           9.44%
    Office Supplies     2.50%

---

### 5. Top 3 Customers in Each Region

Query:

    What are the top 3 customers in each region by revenue?

The engine performs nested ranking independently within each region.

    Region
       |
       v
    Customer
       |
       v
    Revenue
       |
       v
    Rank

---

### 6. Target Comparison

Query:

    Compare actual revenue with target for February 2024.

The system compares actual revenue against regional targets and returns actual revenue, target revenue, difference, achievement percentage and target status.

---

### 7. Monthly Revenue

Query:

    What is the monthly revenue?

Example result:

    2024-01    1146.0
    2024-02    1446.0
    2024-03    3542.4

---

### 8. Year-over-Year Analysis

Query:

    What is the year-over-year revenue growth?

The system first checks whether multiple years of data are available.

If historical data is insufficient, the system does not generate a false YoY percentage.

---

## GenAI Integration

GenAI is used to understand natural-language questions and generate structured analytical query plans.

The AI determines:

- Operation
- Metric
- Aggregation
- Grouping
- Filters
- Ranking
- Time period
- Nested query requirements

The actual numerical calculation is performed by deterministic Python/Pandas logic.

This separates:

    Language Understanding

from:

    Numerical Execution

This improves reliability and reduces the risk of AI-generated numerical errors.

---

## Local Fallback

The application includes a local fallback planner for supported analytical patterns.

The fallback is useful when:

- The external GenAI service is unavailable
- The API is temporarily rate-limited
- Development/testing is performed without relying completely on the external model

Unsupported queries are not given fabricated answers.

---

## Confidence Score

Each successful query receives a confidence score between 0 and 1.

Example:

    confidence_score: 0.9

The frontend displays this score to communicate how confidently the system interpreted the query.

---

## Explanation

Each successful response includes an explanation.

Example:

    The sum of revenue was calculated.

For complex queries, the explanation can describe:

- Grouping
- Ranking
- Filtering
- Comparison
- Time period
- Analytical operation

---

## Unsupported Queries

InsightIQ avoids fabricating results.

For example:

    Which product has the highest profit margin?

If the required analytical logic is not supported, the system returns an appropriate error instead of inventing a result.

This makes the system safer and more reliable for analytics.

---

## API

### Health Check

    GET /api/health

Example response:

    {
      "status": "healthy",
      "service": "InsightIQ"
    }

### Query API

    POST /api/query

Request:

    {
      "query": "What are the total sales?"
    }

Response:

    {
      "query": "What are the total sales?",
      "status": "success",
      "generated_logic": {
        "operation": "sum",
        "metric": "revenue",
        "aggregation": "sum",
        "group_by": [],
        "filters": [],
        "time_period": null,
        "rows_returned": 1
      },
      "result": 6134.4,
      "confidence_score": 0.9,
      "explanation": "The sum of revenue was calculated."
    }

---

## Running the Backend

Open PowerShell:

    cd C:\Users\anshi\OneDrive\Desktop\InsightIQ\backend

Activate the virtual environment:

    .\venv\Scripts\Activate.ps1

Start the backend:

    python -m uvicorn main:app --reload --port 8000

Backend:

    http://127.0.0.1:8000

Health check:

    http://127.0.0.1:8000/api/health

Swagger documentation:

    http://127.0.0.1:8000/docs

---

## Running the Frontend

Open another terminal:

    cd C:\Users\anshi\OneDrive\Desktop\InsightIQ\frontend

Install dependencies:

    npm install

Start the frontend:

    npm run dev

The frontend will normally be available at:

    http://localhost:5173

If port 5173 is already in use, Vite may automatically select another port.

---

## Environment Variables

Create:

    backend/.env

Example:

    GEMINI_API_KEY=your_api_key_here

Do not commit the .env file to GitHub.

The project .gitignore contains:

    node_modules/
    backend/venv/
    __pycache__/
    *.pyc
    .env
    **/init.py

---

## Testing

The backend uses Pytest.

From the backend directory:

    pytest -q

The test suite covers:

- Total sales
- Average Order Value
- Top cities by profit
- Top customers within regions
- Target comparison

Expected result:

    5 passed

---

## Sample Outputs

The sample_outputs directory contains representative JSON responses:

    sample_outputs/
    ├── query_01.json
    ├── query_02.json
    ├── query_03.json
    ├── query_04.json
    └── query_05.json

These demonstrate:

- Aggregation
- Ranking
- AOV
- Target comparison
- Nested ranking

Each sample output contains:

- query
- generated_logic
- result
- confidence_score
- explanation

---

## Design Decisions

### AI for Interpretation

GenAI is used for natural-language understanding and query-plan generation.

It does not directly calculate the final numerical result.

### Deterministic Execution

The analytics engine performs calculations using Pandas.

This provides more reliable and reproducible numerical results.

### Validation Before Execution

Every generated query plan passes through validation before execution.

### Modular Architecture

The backend is separated into:

    AI
    Data
    Engine
    Models
    Services
    API
    Tests

This improves maintainability and makes future extensions easier.

### Safe Failure

When the system cannot safely support a query, it returns an error instead of fabricating an answer.

---

## Trade-offs

### GenAI Flexibility vs Deterministic Execution

GenAI provides flexible natural-language understanding, while deterministic execution provides reliable calculations.

The trade-off is that new analytical patterns may require additional planner and executor logic.

### Local Fallback

The local fallback improves availability when the external AI service is unavailable.

However, it supports a defined set of analytical patterns rather than every possible natural-language query.

### Dataset Scope

The current implementation uses the provided sales and target datasets.

More advanced analytics may require additional fields or larger datasets.

---

## Edge Cases

### Empty Query

An empty query returns an appropriate validation error.

### Unsupported Query

Unsupported analytical questions are rejected instead of returning fabricated results.

### Insufficient Historical Data

For Year-over-Year analysis, the engine checks whether multiple years are available.

### Invalid Query Plan

Invalid AI-generated plans are rejected by the validation layer.

### Missing Dataset

The data loader raises an error when a required dataset file is unavailable.

---

## Assignment Requirement Mapping

| Requirement | Implementation |
|---|---|
| Natural language input | GenAI planner + local fallback |
| Aggregations | Aggregation engine |
| Grouping | Group-by execution |
| Filtering | Filter engine |
| Ranking | Ranking engine |
| Top N within groups | Nested query engine |
| Contribution percentage | Percentage engine |
| Target comparison | Comparison engine |
| Time-based queries | Time analysis engine |
| GenAI usage | AI query-plan generation |
| Confidence score | Confidence service |
| Explanation | Explanation service |
| Error handling | Validation + API error handling |
| Sample outputs | sample_outputs/ |
| Testing | Pytest |
| Feedback loop | Not implemented because no feedback log was provided |

---

## Future Improvements

- More natural-language query patterns
- Advanced filter operators such as >, <, >=, <=
- More complex nested queries
- Automatic schema discovery
- Query history
- User feedback collection
- Feedback-based improvement
- Database-backed analytics
- Larger datasets
- Advanced time-series analysis
- Authentication and authorization
- Production deployment
- Query caching
- More detailed confidence scoring
- Streaming AI responses

---

## Project Highlights

InsightIQ demonstrates a complete end-to-end intelligent analytics workflow:

    Natural Language Query
            |
            v
    GenAI Interpretation
            |
            v
    Structured Query Plan
            |
            v
    Validation
            |
            v
    Deterministic Execution
            |
            v
    Confidence Scoring
            |
            v
    Explanation
            |
            v
    Interactive Result

### Core Design Principle

> Use AI to understand the question, but use deterministic code to calculate the answer.

This provides a balance between natural-language flexibility and analytical reliability.

---

## Conclusion

InsightIQ is an intelligent analytics query engine that allows users to interact with business data using natural language.

Instead of requiring users to write SQL or understand data-processing code, they can ask questions in plain English and receive:

- Structured analytical logic
- Executable query plans
- Accurate results
- Confidence scores
- Human-readable explanations
- Safe handling of unsupported queries

The project combines GenAI, FastAPI, Pandas, React, Recharts, deterministic analytics, query validation, confidence scoring and automated testing into a complete end-to-end analytics application.
