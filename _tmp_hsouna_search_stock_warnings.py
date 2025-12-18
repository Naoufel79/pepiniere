import psycopg

conninfo = "postgresql://postgres:KsgyhdFJGPsfBUHTFRsgRUcHfWmYEvzj@interchange.proxy.rlwy.net:44776/railway"
needle = 'Stock warnings'

with psycopg.connect(conninfo, connect_timeout=15) as con:
    with con.cursor() as cur:
        # Find candidate text columns
        cur.execute("""
            select table_schema, table_name, column_name
            from information_schema.columns
            where table_schema not in ('pg_catalog','information_schema')
              and data_type in ('text','character varying','character')
            order by table_schema, table_name, column_name
        """)
        cols = cur.fetchall()

        hits = []
        for schema, table, col in cols:
            fq = f'"{schema}"."{table}"'
            try:
                cur.execute(f"select count(*) from {fq} where {col} = %s", (needle,))
                n = cur.fetchone()[0]
                if n:
                    hits.append((schema, table, col, n, 'equals'))
                    continue
                cur.execute(f"select count(*) from {fq} where cast({col} as text) ilike %s", (f"%{needle}%",))
                n2 = cur.fetchone()[0]
                if n2:
                    hits.append((schema, table, col, n2, 'ilike'))
            except Exception:
                # ignore columns we can't query (type issues, perms, etc.)
                continue

        print('HITS', len(hits))
        for h in hits:
            print(' -', h)

        # If hits, fetch sample rows to "recopie-la telle quelle"
        for schema, table, col, n, mode in hits:
            fq = f'"{schema}"."{table}"'
            cur.execute(f"select {col} from {fq} where cast({col} as text) ilike %s limit 5", (f"%{needle}%",))
            vals = [r[0] for r in cur.fetchall()]
            print(f"\nSample from {schema}.{table}.{col} ({mode}, {n}):")
            for v in vals:
                print(v)
