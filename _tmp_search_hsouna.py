import sqlite3
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
needle = 'hsouna'
# get tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
found = []
for t in tables:
    cur.execute(f"PRAGMA table_info('{t}')")
    text_cols = [row[1] for row in cur.fetchall() if str(row[2] or '').lower() in ('text','varchar','char')]
    for col in text_cols:
        try:
            cur.execute(f"SELECT COUNT(*) FROM '{t}' WHERE lower(COALESCE({col},'')) LIKE ?", (f"%{needle}%",))
            n = cur.fetchone()[0]
            if n:
                found.append((t, col, n))
        except Exception:
            pass
print('Matches for', needle)
for t,col,n in found:
    print(f" - {t}.{col}: {n}")
con.close()
