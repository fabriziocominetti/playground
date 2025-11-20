from pathlib import Path
from typing import Optional

import pandas as pd


def load_data(file_path: Path) -> Optional[pd.DataFrame]:
    """Load data from a CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(file_path, encoding="latin1")
    except FileNotFoundError:
        print(f"Error: The file was not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


def main():
    """Main function to execute the data processing pipeline."""
    project_root = Path(__file__).resolve().parents[2]
    data_file = "results.csv"
    data_path = project_root / "data" / data_file

    df = load_data(data_path)

    if df is not None:
        print("Data loaded successfully:")
        print(df.head())
    else:
        print("No data to display.")


if __name__ == "__main__":
    main()
