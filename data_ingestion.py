"""
data_ingestion.py
Day 1 - Task 1: Load every CSV in data/raw/, and for each print its
shape, column data types, and first rows to spot anomalies early.
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")


def main():
    csv_files = sorted(RAW_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {RAW_DIR}/")
        return

    print(f"Found {len(csv_files)} CSV file(s) in {RAW_DIR}/\n")

    for path in csv_files:
        print("=" * 70)
        print(f"FILE: {path.name}")
        print("=" * 70)

        df = pd.read_csv(path)

        print(f"shape (rows, cols): {df.shape}\n")
        print("dtypes:")
        print(df.dtypes)
        print("\nhead:")
        print(df.head())
        print("\n")


if __name__ == "__main__":
    main()
