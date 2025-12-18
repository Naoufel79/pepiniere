import sqlite3, os
path = 'db.sqlite3'
print('DB', os.path.abspath(path), os.path.exists(path))
con = sqlite3.connect(path)
cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
print('Tables:')
for (name,) in cur.fetchall():
    print(' -', name)
con.close()
