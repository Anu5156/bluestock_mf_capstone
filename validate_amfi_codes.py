"""
validate_amfi_codes.py
Day 1 - Task 5: Confirm every amfi_code in fund_master exists in
nav_history. Write a short data quality summary to reports/.
"""

import pandas as pd

fm = pd.read_csv("data/raw/01_fund_master.csv")
nav = pd.read_csv("data/raw/02_nav_history.csv")

fm_codes = set(fm["amfi_code"])
nav_codes = set(nav["amfi_code"])

missing_from_nav = fm_codes - nav_codes          # funds with no NAV data
extra_in_nav = nav_codes - fm_codes              # NAV data with no fund record

lines = []
lines.append("DAY 1 - DATA QUALITY SUMMARY")
lines.append("=" * 45)
lines.append(f"Funds in fund_master            : {len(fm_codes)}")
lines.append(f"Distinct codes in nav_history   : {len(nav_codes)}")
lines.append(f"Funds WITH nav history          : {len(fm_codes & nav_codes)}")
lines.append(f"Funds MISSING from nav_history  : {len(missing_from_nav)}")
lines.append(f"Codes in nav but NOT in master  : {len(extra_in_nav)}")
lines.append("")
lines.append(f"Missing codes : {sorted(missing_from_nav)}")
lines.append(f"Orphan codes  : {sorted(extra_in_nav)}")
lines.append("")
lines.append("NOTE (API anomaly): mfapi.in code 125497 is labelled")
lines.append("HDFC Top 100 in the brief but the API returns SBI Small")
lines.append("Cap metadata for it. Flagged during live NAV fetch.")

report = "\n".join(lines)
print(report)

with open("reports/day1_data_quality.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("\nSaved -> reports/day1_data_quality.txt")
