from pathlib import Path
from io import StringIO
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"


def read_quoted_csv(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8-sig") as file:
        lines = file.readlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]

        cleaned_lines.append(line)

    csv_content = "\n".join(cleaned_lines)
    return pd.read_csv(
    StringIO(csv_content),
    sep=",",
    keep_default_na=False
)



def load_sales_data() -> pd.DataFrame:
    file_path = DATASET_DIR / "sales_data.csv"
    return read_quoted_csv(file_path)


def load_targets_data() -> pd.DataFrame:
    file_path = DATASET_DIR / "targets.csv"
    return read_quoted_csv(file_path)