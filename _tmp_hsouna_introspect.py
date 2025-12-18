import psycopg
from pprint import pprint

conninfo = "postgresql://postgres:KsgyhdFJGPsfBUHTFRsgRUcHfWmYEvzj@interchange.proxy.rlwy.net:44776/railway"

with psycopg.connect(conninfo, connect_timeout=15) as con:
    with con.cursor() as cur:
        cur.execute('select current_database(), current_user')
        print('DB/User:', cur.fetchone())

        cur.execute("""
            select table_schema, table_name
            from information_schema.tables
            where table_schema not in ('pg_catalog','information_schema')
            order by table_schema, table_name
        """)
        tables = cur.fetchall()
        print('\nTables:', len(tables))
        for s,n in tables:
            print(' -', f"{s}.{n}")

        cur.execute("""
            select table_schema, table_name
            from information_schema.views
            where table_schema not in ('pg_catalog','information_schema')
            order by table_schema, table_name
        """)
        views = cur.fetchall()
        print('\nViews:', len(views))
        for s,n in views:
            print(' -', f"{s}.{n}")
