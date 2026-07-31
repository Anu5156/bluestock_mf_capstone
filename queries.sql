-- queries.sql
-- Day 2 - Task 6: 10 analytical queries against bluestock_mf.db

-- 1. Top 5 funds by latest AUM (from performance table)
SELECT f.scheme_name, f.fund_house, p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 5;

-- 2. Average NAV per month for each fund
SELECT amfi_code,
       strftime('%Y-%m', date) AS month,
       ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- 3. Total AUM per fund house (latest snapshot)
SELECT fund_house,
       SUM(aum_crore) AS total_aum_crore,
       SUM(num_schemes) AS total_schemes
FROM fact_aum
WHERE date = (SELECT MAX(date) FROM fact_aum)
GROUP BY fund_house
ORDER BY total_aum_crore DESC;

-- 4. Transactions grouped by state
SELECT state,
       COUNT(*) AS num_transactions,
       SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. Funds with expense ratio under 1%
SELECT f.scheme_name, f.fund_house, p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct;

-- 6. Transaction count by type (SIP / Lumpsum / Redemption)
SELECT transaction_type,
       COUNT(*) AS num_transactions,
       SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;

-- 7. Fund count by category and sub-category
SELECT category, sub_category, COUNT(*) AS num_funds
FROM dim_fund
GROUP BY category, sub_category
ORDER BY category, num_funds DESC;

-- 8. Top 10 funds by 5-year return
SELECT f.scheme_name, f.fund_house, p.return_5yr_pct
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.return_5yr_pct IS NOT NULL
ORDER BY p.return_5yr_pct DESC
LIMIT 10;

-- 9. Transactions by KYC status
SELECT kyc_status,
       COUNT(*) AS num_transactions
FROM fact_transactions
GROUP BY kyc_status;

-- 10. Latest NAV per fund (most recent date)
SELECT n.amfi_code, f.scheme_name, n.date, n.nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
WHERE n.date = (SELECT MAX(date) FROM fact_nav n2 WHERE n2.amfi_code = n.amfi_code)
ORDER BY n.nav DESC;
