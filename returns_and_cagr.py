"""
returns_and_cagr.py
Day 4 - Tasks 1 & 2: Compute daily returns and CAGR (1/3/5 yr) for all funds.
"""
import pandas as pd
import numpy as np

nav = pd.read_csv("data/processed/nav_history_clean.csv", parse_dates=["date"])
nav = nav.sort_values(["amfi_code", "date"])
funds = pd.read_csv("data/raw/01_fund_master.csv")

# ---------- Task 1: daily returns ----------
nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change()

print("=" * 55)
print("TASK 1: DAILY RETURNS")
print("=" * 55)
print("Total return observations:", nav["daily_return"].notna().sum())
print("\nDistribution summary (sanity check):")
print(nav["daily_return"].describe())
# reasonable = most daily returns tiny (near 0), std small (~1-2%)
print("\nExtreme daily moves (should be rare):")
print("  returns > +20% :", (nav["daily_return"] > 0.20).sum())
print("  returns < -20% :", (nav["daily_return"] < -0.20).sum())

# save the daily returns
nav.to_csv("data/processed/nav_with_returns.csv", index=False)
print("\nSaved -> data/processed/nav_with_returns.csv")

# ---------- Task 2: CAGR for 1yr, 3yr, 5yr ----------
print("\n" + "=" * 55)
print("TASK 2: CAGR COMPARISON TABLE")
print("=" * 55)

def cagr_for_years(group, years):
    """CAGR over the last `years` years for one fund."""
    end_date = group["date"].max()
    start_date = end_date - pd.DateOffset(years=years)
    window = group[group["date"] >= start_date]
    if len(window) < 2:
        return np.nan
    nav_start = window.iloc[0]["nav"]
    nav_end = window.iloc[-1]["nav"]
    if nav_start <= 0:
        return np.nan
    return (nav_end / nav_start) ** (1 / years) - 1

rows = []
for code, group in nav.groupby("amfi_code"):
    rows.append({
        "amfi_code": code,
        "cagr_1yr_pct": round(cagr_for_years(group, 1) * 100, 2),
        "cagr_3yr_pct": round(cagr_for_years(group, 3) * 100, 2),
        "cagr_5yr_pct": round(cagr_for_years(group, 5) * 100, 2),
    })

cagr_table = pd.DataFrame(rows)
# add fund names for readability
cagr_table = cagr_table.merge(
    funds[["amfi_code", "scheme_name", "category"]], on="amfi_code", how="left")
cagr_table = cagr_table[["amfi_code", "scheme_name", "category",
                          "cagr_1yr_pct", "cagr_3yr_pct", "cagr_5yr_pct"]]

print(cagr_table.to_string(index=False))
cagr_table.to_csv("data/processed/cagr_comparison.csv", index=False)
print("\nSaved -> data/processed/cagr_comparison.csv")
