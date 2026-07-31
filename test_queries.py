import sqlite3
with open("queries.sql", encoding="utf-8-sig") as f:
    sql = f.read()

conn = sqlite3.connect("bluestock_mf.db")
cur = conn.cursor()

# split on the comment markers to run each query
queries = [q for q in sql.split(";") if q.strip() and not q.strip().startswith("--\n")]
for i, q in enumerate(queries, 1):
    if not q.strip():
        continue
    try:
        cur.execute(q)
        rows = cur.fetchall()
        print(f"\n--- Query {i} --- ({len(rows)} rows, showing first 3)")
        for r in rows[:3]:
            print(r)
    except Exception as e:
        print(f"\n--- Query {i} FAILED: {e}")
conn.close()
