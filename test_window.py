import sqlite3
conn = sqlite3.connect("bluestock_mf.db")
cur = conn.cursor()
q = """
SELECT f.category, f.scheme_name, p.return_3yr_pct,
       RANK() OVER (PARTITION BY f.category ORDER BY p.return_3yr_pct DESC) AS rank_in_category
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY f.category, rank_in_category
LIMIT 15;
"""
for row in cur.execute(q):
    print(row)
conn.close()
