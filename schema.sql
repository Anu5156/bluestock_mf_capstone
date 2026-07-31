-- schema.sql
-- Day 2 - Task 4: Star schema for Bluestock MF analytics (SQLite)

-- ---------- DIMENSION TABLES ----------

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code          INTEGER PRIMARY KEY,
    fund_house         TEXT,
    scheme_name        TEXT,
    category           TEXT,
    sub_category       TEXT,
    plan               TEXT,
    risk_category      TEXT,
    sebi_category_code TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    date       TEXT UNIQUE,
    year       INTEGER,
    month      INTEGER,
    day        INTEGER
);

-- ---------- FACT TABLES ----------

CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code   INTEGER,
    date        TEXT,
    nav         REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id        TEXT,
    amfi_code          INTEGER,
    transaction_date   TEXT,
    transaction_type   TEXT,
    amount_inr         INTEGER,
    state              TEXT,
    city               TEXT,
    kyc_status         TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_performance (
    perf_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code          INTEGER,
    return_1yr_pct     REAL,
    return_3yr_pct     REAL,
    return_5yr_pct     REAL,
    sharpe_ratio       REAL,
    expense_ratio_pct  REAL,
    risk_grade         TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    date         TEXT,
    fund_house   TEXT,
    aum_crore    INTEGER,
    num_schemes  INTEGER
);
