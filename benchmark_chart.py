"""
benchmark_chart.py
Day 4 - Task 8: Top 5 funds vs NIFTY50 & NIFTY100 over 3 years + tracking error.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

nav = pd.read_csv("data/processed/nav_history_clean.csv", parse_dates=["date"])
bench = pd.read_csv("data/raw/10_benchmark_indices.csv", parse_dates=["date"])
score = pd.read_csv("data/processed/fund_scorecard.csv")
funds = pd.read_csv("data/raw/01_fund_master.csv")

# top 5 funds by scorecard
top5_names = score.head(5)["scheme_name"].tolist()
top5 = funds[funds["scheme_name"].isin(top5_names)][["amfi_code","scheme_name"]]

# last 3 years
cutoff = nav["date"].max() - pd.DateOffset(years=3)

plt.figure(figsize=(14, 7))

# plot each top fund (normalized to 100 at start)
for _, row in top5.iterrows():
    f = nav[(nav["amfi_code"]==row["amfi_code"]) & (nav["date"]>=cutoff)].sort_values("date")
    if len(f) == 0: continue
    norm = f["nav"] / f["nav"].iloc[0] * 100
    plt.plot(f["date"], norm, label=row["scheme_name"][:30])

# plot benchmarks (normalized)
for idx, style in [("NIFTY50","--"), ("NIFTY100","--")]:
    b = bench[(bench["index_name"]==idx) & (bench["date"]>=cutoff)].sort_values("date")
    if len(b) == 0: continue
    norm = b["close_value"] / b["close_value"].iloc[0] * 100
    plt.plot(b["date"], norm, style, linewidth=2, label=idx)

plt.title("Top 5 Funds vs NIFTY50 & NIFTY100 (3 Years, normalized to 100)")
plt.ylabel("Growth of 100"); plt.legend(fontsize=8); plt.tight_layout()
plt.savefig("reports/charts/10_benchmark_comparison.png", dpi=120)
plt.show()
print("Saved chart -> reports/charts/10_benchmark_comparison.png")

# tracking error vs NIFTY100
print("\nTracking error vs NIFTY100:")
nav_ret = nav.sort_values(["amfi_code","date"]).copy()
nav_ret["ret"] = nav_ret.groupby("amfi_code")["nav"].pct_change()
n100 = bench[bench["index_name"]=="NIFTY100"].sort_values("date").copy()
n100["bret"] = n100["close_value"].pct_change()
for _, row in top5.iterrows():
    f = nav_ret[nav_ret["amfi_code"]==row["amfi_code"]][["date","ret"]]
    m = f.merge(n100[["date","bret"]], on="date", how="inner").dropna()
    te = (m["ret"] - m["bret"]).std() * np.sqrt(252)
    print(f"  {row['scheme_name'][:35]}: {te:.3f}")
