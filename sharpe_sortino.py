"""
sharpe_sortino.py
Day 4 - Tasks 3 & 4: Sharpe and Sortino ratios, ranked.
"""
import pandas as pd
import numpy as np

RF = 0.065      # risk-free rate (RBI repo proxy)
TD = 252        # trading days/year

nav = pd.read_csv("data/processed/nav_with_returns.csv", parse_dates=["date"])
funds = pd.read_csv("data/raw/01_fund_master.csv")

def sharpe(r):
    r = r.dropna()
    if len(r) < 2 or r.std() == 0: return np.nan
    return (r.mean()*TD - RF) / (r.std()*np.sqrt(TD))

def sortino(r):
    r = r.dropna()
    down = r[r < 0]
    if len(down) < 2 or down.std() == 0: return np.nan
    return (r.mean()*TD - RF) / (down.std()*np.sqrt(TD))

rows = []
for code, g in nav.groupby("amfi_code"):
    rows.append({
        "amfi_code": code,
        "sharpe": round(sharpe(g["daily_return"]), 3),
        "sortino": round(sortino(g["daily_return"]), 3),
    })

m = pd.DataFrame(rows).merge(
    funds[["amfi_code","scheme_name","category"]], on="amfi_code", how="left")
m["sharpe_rank"] = m["sharpe"].rank(ascending=False)
m = m.sort_values("sharpe_rank")

print("TASKS 3-4: Sharpe & Sortino, top 10 by Sharpe:")
print(m[["scheme_name","category","sharpe","sharpe_rank","sortino"]].head(10).to_string(index=False))
m.to_csv("data/processed/sharpe_sortino.csv", index=False)
print("\nSaved -> data/processed/sharpe_sortino.csv")
