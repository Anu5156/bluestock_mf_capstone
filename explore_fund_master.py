"""
explore_fund_master.py
Day 1 - Task 4: Explore fund_master. Print unique fund houses,
categories, sub-categories, and risk categories, plus a look at the
AMFI code structure.
"""

import pandas as pd

fm = pd.read_csv("data/raw/01_fund_master.csv")

print("shape (rows, cols):", fm.shape)
print("columns:", list(fm.columns), "\n")

for col in ["fund_house", "category", "sub_category", "risk_category"]:
    print("=" * 55)
    print(f"UNIQUE VALUES IN: {col}   (count = {fm[col].nunique()})")
    print("=" * 55)
    print(fm[col].value_counts())
    print()

# ---- AMFI code structure ----
print("=" * 55)
print("AMFI CODE STRUCTURE")
print("=" * 55)
print("total funds        :", len(fm))
print("unique amfi_codes  :", fm["amfi_code"].nunique())
print("min amfi_code      :", fm["amfi_code"].min())
print("max amfi_code      :", fm["amfi_code"].max())
print("any duplicate codes:", fm["amfi_code"].duplicated().any())
print("\nFund count per house:")
print(fm.groupby("fund_house")["amfi_code"].count().sort_values(ascending=False))
