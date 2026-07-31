"""
day2_additions.py
Adds two details the Day 2 spec names specifically:
- Flag negative Sharpe ratios (Task 3)
- Add daily_return to fact_nav (Task 4/5)
"""
import pandas as pd
from sqlalchemy import create_engine, text

# --- Task 3: flag negative Sharpe ratios ---
perf = pd.read_csv("data/processed/scheme_performance_clean.csv")
neg_sharpe = perf[perf["sharpe_ratio"] < 0]
print(f"Funds with NEGATIVE Sharpe ratio: {len(neg_sharpe)}")
if len(neg_sharpe):
    print(neg_sharpe[["amfi_code", "scheme_name", "sharpe_ratio"]].to_string(index=False))

# --- Task 4/5: add daily_return to fact_nav ---
engine = create_engine("sqlite:///bluestock_mf.db")
nav = pd.read_csv("data/processed/nav_history_clean.csv", parse_dates=["date"])
nav = nav.sort_values(["amfi_code", "date"])
# daily return = pct change in NAV within each fund
nav["daily_return"] = nav.groupby("amfi_code")["nav"].pct_change() * 100
nav["date"] = nav["date"].dt.strftime("%Y-%m-%d")
nav[["amfi_code", "date", "nav", "daily_return"]].to_sql(
    "fact_nav", engine, if_exists="replace", index=False)
print("\nfact_nav rebuilt with daily_return column.")

# verify
with engine.connect() as conn:
    sample = conn.execute(text(
        "SELECT amfi_code, date, nav, daily_return FROM fact_nav "
        "WHERE daily_return IS NOT NULL LIMIT 5")).fetchall()
    print("Sample rows:")
    for r in sample:
        print(r)
