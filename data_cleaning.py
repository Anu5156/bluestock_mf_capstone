"""
data_cleaning.py
Day 2 - Tasks 1-3: Clean nav_history, investor_transactions, and
scheme_performance. Save cleaned versions to data/processed/.
"""

import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)


def clean_nav_history():
    print("Cleaning nav_history...")
    df = pd.read_csv(RAW / "02_nav_history.csv")

    # parse dates, sort, drop duplicates
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["amfi_code", "date"])
    df = df.drop_duplicates(subset=["amfi_code", "date"])

    # forward-fill NAV within each fund (holidays/weekends)
    df["nav"] = df.groupby("amfi_code")["nav"].ffill()

    # validate NAV > 0
    before = len(df)
    df = df[df["nav"] > 0]
    print(f"  removed {before - len(df)} rows with NAV <= 0")

    df.to_csv(OUT / "nav_history_clean.csv", index=False)
    print(f"  saved {len(df)} rows")


def clean_investor_transactions():
    print("Cleaning investor_transactions...")
    df = pd.read_csv(RAW / "08_investor_transactions.csv")

    # standardise transaction_type
    df["transaction_type"] = df["transaction_type"].str.strip().str.title()
    print("  transaction_type values:", df["transaction_type"].unique())

    # fix dates, validate amount > 0
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    before = len(df)
    df = df[df["amount_inr"] > 0]
    print(f"  removed {before - len(df)} rows with amount <= 0")

    # check KYC enum values
    print("  kyc_status values:", df["kyc_status"].unique())

    df.to_csv(OUT / "investor_transactions_clean.csv", index=False)
    print(f"  saved {len(df)} rows")


def clean_scheme_performance():
    print("Cleaning scheme_performance...")
    df = pd.read_csv(RAW / "07_scheme_performance.csv")

    # validate return columns are numeric
    for col in ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # flag expense_ratio outside 0.1% - 2.5%
    out_of_range = df[(df["expense_ratio_pct"] < 0.1) | (df["expense_ratio_pct"] > 2.5)]
    print(f"  {len(out_of_range)} rows with expense_ratio outside 0.1-2.5%")

    df.to_csv(OUT / "scheme_performance_clean.csv", index=False)
    print(f"  saved {len(df)} rows")


if __name__ == "__main__":
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    print("\nDone. Cleaned files are in data/processed/")
