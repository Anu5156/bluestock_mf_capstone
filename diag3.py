import pandas as pd

nav = pd.read_csv("data/processed/nav_history_clean.csv", parse_dates=["date"])
bench = pd.read_csv("data/raw/10_benchmark_indices.csv", parse_dates=["date"])

# recompute fund returns FRESH from clean NAV
nav = nav.sort_values(["amfi_code","date"])
nav["ret"] = nav.groupby("amfi_code")["nav"].pct_change()

nifty = bench[bench["index_name"]=="NIFTY100"].sort_values("date").copy()
nifty["bret"] = nifty["close_value"].pct_change()

# test 3 different funds
for code in nav["amfi_code"].unique()[:3]:
    one = nav[nav["amfi_code"]==code][["date","ret"]]
    m = one.merge(nifty[["date","bret"]], on="date", how="inner").dropna()
    print(f"Fund {code}: n={len(m)}, correlation={m['ret'].corr(m['bret']):.3f}")
