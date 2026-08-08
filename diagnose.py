import pandas as pd
nav = pd.read_csv("data/processed/nav_with_returns.csv", parse_dates=["date"])
bench = pd.read_csv("data/raw/10_benchmark_indices.csv", parse_dates=["date"])
nifty = bench[bench["index_name"] == "NIFTY100"].sort_values("date").copy()
nifty["bench_return"] = nifty["close_value"].pct_change()

# take one fund
one = nav[nav["amfi_code"] == nav["amfi_code"].iloc[0]].sort_values("date")
print("Fund dates sample:", one["date"].head(3).tolist())
print("Bench dates sample:", nifty["date"].head(3).tolist())
print("Fund date dtype:", one["date"].dtype)
print("Bench date dtype:", nifty["date"].dtype)

merged = one[["date","daily_return"]].merge(nifty[["date","bench_return"]], on="date", how="inner")
print("Rows after merge:", len(merged))
print("Non-null both:", merged.dropna().shape[0])
print(merged.dropna().head())
