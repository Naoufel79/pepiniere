import psycopg
import sys

conninfo = "postgresql://external_client:Ext3rn4lCl13nt!2025$@interchange.proxy.rlwy.net:44776/railway"

print('Connecting...')
with psycopg.connect(conninfo, connect_timeout=10) as con:
    with con.cursor() as cur:
        cur.execute('select current_database(), current_user, version()')
        print('DB:', cur.fetchone()[0])
        cur.execute("select table_schema, table_name from information_schema.tables where table_schema not in ('pg_catalog','information_schema') order by table_schema, table_name")
        tables = cur.fetchall()
        print('Tables:', len(tables))
        for s,n in tables[:50]:
            print(' -', s+'.'+n)
        if len(tables) > 50:
            print(' ...')
        cur.execute("select table_schema, table_name from information_schema.views where table_schema not in ('pg_catalog','information_schema') order by table_schema, table_name")
        views = cur.fetchall()
        print('Views:', len(views))
        for s,n in views[:80]:
            print(' -', s+'.'+n)
        if len(views) > 80:
            print(' ...')

print('OK')
