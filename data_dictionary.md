# Data Dictionary — Bluestock MF Analytics

Documentation of all tables and columns in `bluestock_mf.db` (SQLite star schema).
Source data: 10 provided CSVs + live NAV from mfapi.in (Day 1), cleaned in Day 2.

---

## dim_fund (dimension)
One row per mutual fund scheme. Source: `01_fund_master.csv`.

| Column | Type | Definition |
|---|---|---|
| amfi_code | INTEGER (PK) | Unique AMFI scheme code identifying the fund |
| fund_house | TEXT | Asset management company (e.g. SBI Mutual Fund) |
| scheme_name | TEXT | Full name of the fund scheme |
| category | TEXT | Broad category (Equity / Debt) |
| sub_category | TEXT | Sub-category (Large Cap, Small Cap, Liquid, etc.) |
| plan | TEXT | Plan type (Regular / Direct) |
| risk_category | TEXT | Risk grade (Low, Moderate, High, Very High) |
| sebi_category_code | TEXT | SEBI classification code |

## dim_date (dimension)
One row per unique trading date. Source: derived from NAV history.

| Column | Type | Definition |
|---|---|---|
| date_id | INTEGER (PK) | Surrogate key for the date |
| date | TEXT | Calendar date (YYYY-MM-DD) |
| year | INTEGER | Year component |
| month | INTEGER | Month component (1-12) |
| day | INTEGER | Day component |

## fact_nav (fact)
Daily Net Asset Value per fund. Source: `02_nav_history.csv` (cleaned).

| Column | Type | Definition |
|---|---|---|
| nav_id | INTEGER (PK) | Surrogate key |
| amfi_code | INTEGER (FK) | Fund reference -> dim_fund |
| date | TEXT | NAV date (YYYY-MM-DD) |
| nav | REAL | Net Asset Value per unit (forward-filled for non-trading days) |

## fact_transactions (fact)
Individual investor transactions. Source: `08_investor_transactions.csv` (cleaned).

| Column | Type | Definition |
|---|---|---|
| transaction_id | INTEGER (PK) | Surrogate key |
| investor_id | TEXT | Anonymised investor identifier |
| amfi_code | INTEGER (FK) | Fund reference -> dim_fund |
| transaction_date | TEXT | Date of transaction |
| transaction_type | TEXT | SIP / Lumpsum / Redemption (standardised) |
| amount_inr | INTEGER | Transaction amount in INR (validated > 0) |
| state | TEXT | Investor state |
| city | TEXT | Investor city |
| kyc_status | TEXT | KYC status (Verified / Pending) |

## fact_performance (fact)
Performance metrics per fund. Source: `07_scheme_performance.csv` (cleaned).

| Column | Type | Definition |
|---|---|---|
| perf_id | INTEGER (PK) | Surrogate key |
| amfi_code | INTEGER (FK) | Fund reference -> dim_fund |
| return_1yr_pct | REAL | 1-year return (%) |
| return_3yr_pct | REAL | 3-year return (%) |
| return_5yr_pct | REAL | 5-year return (%) |
| sharpe_ratio | REAL | Risk-adjusted return measure |
| expense_ratio_pct | REAL | Annual expense ratio (%), validated 0.1-2.5 |
| risk_grade | TEXT | Risk grade label |

## fact_aum (fact)
Assets Under Management by fund house over time. Source: `03_aum_by_fund_house.csv`.

| Column | Type | Definition |
|---|---|---|
| aum_id | INTEGER (PK) | Surrogate key |
| date | TEXT | Snapshot date |
| fund_house | TEXT | Asset management company |
| aum_crore | INTEGER | Assets under management (INR crore) |
| num_schemes | INTEGER | Number of schemes offered |

---

## Data Quality Notes
- Live NAV fetch (Day 1): 4 of 6 scheme codes in the brief return a different fund from mfapi.in than their label. See `reports/day1_data_quality.txt`.
- NAV values forward-filled within each fund for weekends/holidays.
- Transaction amounts and NAV values validated as > 0 during cleaning.
