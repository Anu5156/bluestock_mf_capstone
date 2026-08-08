"""
fund_scorecard.py
Day 4 - Task 7: Composite 0-100 scorecard.
30% 3yr return + 25% Sharpe + 20% Alpha + 15% expense (inverse) + 10% maxDD (inverse)
"""
import pandas as pd

funds = pd.read_csv("data/raw/01_fund_master.csv")
perf = pd.read_csv("data/raw/07_scheme_performance.csv")  # has return_3yr, expense_ratio
sharpe = pd.read_csv("data/processed/sharpe_sortino.csv")
alpha = pd.read_csv("data/processed/alpha_beta.csv")
dd = pd.read_csv("data/processed/max_drawdown.csv")

# start from fund list
s = funds[["amfi_code", "scheme_name", "category"]].copy()

# merge in each metric (by amfi_code where available, else by scheme_name)
s = s.merge(perf[["amfi_code", "return_3yr_pct", "expense_ratio_pct"]], on="amfi_code", how="left")
s = s.merge(sharpe[["amfi_code", "sharpe"]], on="amfi_code", how="left")
s = s.merge(alpha[["scheme_name", "alpha"]], on="scheme_name", how="left")
s = s.merge(dd[["scheme_name", "max_drawdown_pct"]], on="scheme_name", how="left")

# rank each (higher metric = better rank, except expense & drawdown where lower/less-negative is better)
n = len(s)
s["r_return"] = s["return_3yr_pct"].rank(ascending=True)       # higher return better
s["r_sharpe"] = s["sharpe"].rank(ascending=True)               # higher sharpe better
s["r_alpha"]  = s["alpha"].rank(ascending=True)                # higher alpha better
s["r_expense"] = s["expense_ratio_pct"].rank(ascending=False)  # lower expense better (inverse)
s["r_dd"] = s["max_drawdown_pct"].rank(ascending=True)         # less negative DD better

# composite score, scaled to 0-100
s["raw"] = (0.30*s["r_return"] + 0.25*s["r_sharpe"] + 0.20*s["r_alpha"]
            + 0.15*s["r_expense"] + 0.10*s["r_dd"])
s["score"] = round((s["raw"] / n) * 100, 1)

out = s[["scheme_name","category","return_3yr_pct","sharpe","alpha",
         "expense_ratio_pct","max_drawdown_pct","score"]].sort_values("score", ascending=False)

print("TASK 7 - Fund Scorecard (top 10):")
print(out.head(10).to_string(index=False))
out.to_csv("data/processed/fund_scorecard.csv", index=False)
print("\nSaved -> data/processed/fund_scorecard.csv")
