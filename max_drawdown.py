"""
max_drawdown.py
Day 4 - Task 6: Maximum drawdown per fund + worst drawdown date range.
"""
import pandas as pd

nav = pd.read_csv("data/processed/nav_history_clean.csv", parse_dates=["date"])
nav = nav.sort_values(["amfi_code", "date"])
funds = pd.read_csv("data/raw/01_fund_master.csv")

rows = []
for code, g in nav.groupby("amfi_code"):
    g = g.copy()
    g["running_max"] = g["nav"].cummax()
    g["drawdown"] = g["nav"] / g["running_max"] - 1
    max_dd = g["drawdown"].min()
    trough_row = g.loc[g["drawdown"].idxmin()]
    trough_date = trough_row["date"]
    peak_nav = trough_row["running_max"]
    peak_date = g[(g["nav"] == peak_nav) & (g["date"] <= trough_date)]["date"].min()
    rows.append({
        "amfi_code": code,
        "max_drawdown_pct": round(max_dd * 100, 2),
        "peak_date": peak_date.date() if pd.notna(peak_date) else None,
        "trough_date": trough_date.date(),
    })

dd = pd.DataFrame(rows).merge(
    funds[["amfi_code","scheme_name","category"]], on="amfi_code", how="left")
dd = dd[["scheme_name","category","max_drawdown_pct","peak_date","trough_date"]].sort_values("max_drawdown_pct")

print("TASK 6 - Maximum Drawdown (worst 10):")
print(dd.head(10).to_string(index=False))
dd.to_csv("data/processed/max_drawdown.csv", index=False)
print("\nSaved -> data/processed/max_drawdown.csv")
