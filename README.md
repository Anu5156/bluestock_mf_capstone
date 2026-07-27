# Bluestock MF Analytics Capstone

Analysis of Indian mutual fund data: fund master, NAV history,
inflows, holdings, and performance.

## Setup
1. Create and activate a virtual environment:
   python -m venv venv
   venv\Scripts\Activate.ps1
2. Install dependencies: pip install -r requirements.txt

## Day 1 - Data Ingestion
- data_ingestion.py - loads and inspects all 10 provided CSVs
- live_nav_fetch.py - fetches live NAV for 6 schemes from mfapi.in
- explore_fund_master.py - EDA on the fund master
- validate_amfi_codes.py - validates AMFI codes, writes data quality report
- notebooks/day1_eda.ipynb - fund master EDA in notebook form

## Data
- data/raw/ - raw datasets (provided CSVs + fetched NAV)
- reports/ - data quality summary

## Known Issues
- 4 of 6 live NAV scheme codes in the brief return a different fund
  from the API than their label (see reports/day1_data_quality.txt).
