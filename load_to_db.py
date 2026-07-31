"""
load_to_db.py
Day 2 - Task 5: Create bluestock_mf.db from schema.sql and load
cleaned + raw data into the star schema. Verify row counts.
"""

import pandas as pd
from sqlalchemy import create_engine, text

RAW = "data/raw"
PROC = "data/processed"
DB = "bluestock_mf.db"

engine = create_engine(f"sqlite:///{DB}")

# 1. Build tables from schema.sql
print("Creating tables from schema.sql...")
with open("sql/schema.sql", encoding="utf-8-sig") as f:
    schema = f.read()
with engine.begin() as conn:
    for statement in schema.split(";"):
        if statement.strip():
            conn.execute(text(statement))

# 2. Load dimension: funds (from raw fund_master)
fund = pd.read_csv(f"{RAW}/01_fund_master.csv")
fund_cols = ["amfi_code", "fund_house", "scheme_name", "category",
             "sub_category", "plan", "risk_category", "sebi_category_code"]
fund[fund_cols].to_sql("dim_fund", engine, if_exists="replace", index=False)
print(f"dim_fund loaded: {len(fund)} rows")

# 3. Load dimension: dates (built from nav dates)
nav = pd.read_csv(f"{PROC}/nav_history_clean.csv", parse_dates=["date"])
dates = pd.DataFrame({"date": nav["date"].dt.strftime("%Y-%m-%d").unique()})
dates["date"] = pd.to_datetime(dates["date"])
dates["year"] = dates["date"].dt.year
dates["month"] = dates["date"].dt.month
dates["day"] = dates["date"].dt.day
dates["date"] = dates["date"].dt.strftime("%Y-%m-%d")
dates.to_sql("dim_date", engine, if_exists="replace", index=False)
print(f"dim_date loaded: {len(dates)} rows")

# 4. Load fact: nav
nav["date"] = nav["date"].dt.strftime("%Y-%m-%d")
nav[["amfi_code", "date", "nav"]].to_sql("fact_nav", engine, if_exists="replace", index=False)
print(f"fact_nav loaded: {len(nav)} rows")

# 5. Load fact: transactions
tx = pd.read_csv(f"{PROC}/investor_transactions_clean.csv")
tx_cols = ["investor_id", "amfi_code", "transaction_date", "transaction_type",
           "amount_inr", "state", "city", "kyc_status"]
tx[tx_cols].to_sql("fact_transactions", engine, if_exists="replace", index=False)
print(f"fact_transactions loaded: {len(tx)} rows")

# 6. Load fact: performance
perf = pd.read_csv(f"{PROC}/scheme_performance_clean.csv")
perf_cols = ["amfi_code", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
             "sharpe_ratio", "expense_ratio_pct", "risk_grade"]
perf[perf_cols].to_sql("fact_performance", engine, if_exists="replace", index=False)
print(f"fact_performance loaded: {len(perf)} rows")

# 7. Load fact: aum
aum = pd.read_csv(f"{RAW}/03_aum_by_fund_house.csv")
aum_cols = ["date", "fund_house", "aum_crore", "num_schemes"]
aum[aum_cols].to_sql("fact_aum", engine, if_exists="replace", index=False)
print(f"fact_aum loaded: {len(aum)} rows")

# 8. Verify
print("\nRow count verification:")
with engine.connect() as conn:
    for table in ["dim_fund", "dim_date", "fact_nav", "fact_transactions",
                  "fact_performance", "fact_aum"]:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"  {table}: {count} rows")

print(f"\nDone. Database created: {DB}")


