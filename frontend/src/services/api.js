const API_URL = "http://127.0.0.1:8000";

export async function analyzeQuery(query) {
  if (!query || !query.trim()) {
    throw new Error("Please enter an analytics question.");
  }

  const response = await fetch(`${API_URL}/api/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: query.trim(),
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Query processing failed."
    );
  }

  return data;
}

export async function checkHealth() {
  const response = await fetch(
    `${API_URL}/api/health`
  );

  if (!response.ok) {
    throw new Error("Backend is not available.");
  }

  return response.json();
}