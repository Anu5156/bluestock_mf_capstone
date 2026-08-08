"""
alpha_beta.py
Day 4 - Task 5: Alpha & Beta via OLS regression of fund daily returns
on NIFTY100 daily returns (scipy.stats.linregress).
"""
import pandas as pd
import numpy as np
from scipy import stats

TD = 252

# fund returns
nav = pd.read_csv("data/processed/nav_with_returns.csv", parse_dates=["date"])
funds = pd.read_csv("data/raw/01_fund_master.csv")

# benchmark: extract NIFTY100 and compute its daily returns
bench = pd.read_csv("data/raw/10_benchmark_indices.csv", parse_dates=["date"])
nifty = bench[bench["index_name"] == "NIFTY100"].sort_values("date").copy()
nifty["bench_return"] = nifty["close_value"].pct_change()
nifty = nifty[["date", "bench_return"]]

rows = []
for code, g in nav.groupby("amfi_code"):
    g = g.sort_values("date")[["date", "daily_return"]]
    # align fund returns with benchmark returns on the same dates
    merged = g.merge(nifty, on="date", how="inner").dropna()
    if len(merged) < 30:
        rows.append({"amfi_code": code, "alpha": np.nan, "beta": np.nan, "r_squared": np.nan})
        continue
    # regression: fund_return = alpha + beta * bench_return
    result = stats.linregress(merged["bench_return"], merged["daily_return"])
    rows.append({
        "amfi_code": code,
        "alpha": round(result.intercept * TD, 4),   # annualized alpha
        "beta": round(result.slope, 3),
        "r_squared": round(result.rvalue ** 2, 3),
    })

ab = pd.DataFrame(rows).merge(
    funds[["amfi_code","scheme_name","category"]], on="amfi_code", how="left")
ab = ab[["scheme_name","category","alpha","beta","r_squared"]].sort_values("alpha", ascending=False)

print("TASK 5 - Alpha & Beta (top 10 by alpha):")
print(ab.head(10).to_string(index=False))
ab.to_csv("data/processed/alpha_beta.csv", index=False)
print("\nSaved -> data/processed/alpha_beta.csv")
