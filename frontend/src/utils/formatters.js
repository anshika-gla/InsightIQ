export function formatNumber(value) {
  if (value === null || value === undefined) {
    return "-";
  }

  if (typeof value !== "number") {
    return value;
  }

  return Number(value.toFixed(2)).toLocaleString();
}

export function formatPercentage(value) {
  if (value === null || value === undefined) {
    return "-";
  }

  return `${Number(value).toFixed(2)}%`;
}

export function formatColumnName(column) {
  if (!column) {
    return "";
  }

  return column
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase()
    );
}