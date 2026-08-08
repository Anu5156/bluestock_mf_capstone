import pandas as pd
from scipy import stats

nav = pd.read_csv("data/processed/nav_with_returns.csv", parse_dates=["date"])
bench = pd.read_csv("data/raw/10_benchmark_indices.csv", parse_dates=["date"])
nifty = bench[bench["index_name"] == "NIFTY100"].sort_values("date").copy()
nifty["bench_return"] = nifty["close_value"].pct_change()

one = nav[nav["amfi_code"] == nav["amfi_code"].iloc[0]].sort_values("date")
merged = one[["date","daily_return"]].merge(
    nifty[["date","bench_return"]], on="date", how="inner").dropna()

print("Data points:", len(merged))
print("Correlation:", merged["daily_return"].corr(merged["bench_return"]))

# regression
res = stats.linregress(merged["bench_return"], merged["daily_return"])
print("slope (beta):", res.slope)
print("intercept:", res.intercept)
print("r_value:", res.rvalue)
print("r_squared:", res.rvalue**2)
