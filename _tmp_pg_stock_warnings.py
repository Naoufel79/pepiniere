import psycopg
from pprint import pprint

conninfo = "postgresql://external_client:Ext3rn4lCl13nt!2025$@interchange.proxy.rlwy.net:44776/railway"

with psycopg.connect(conninfo, connect_timeout=10) as con:
    with con.cursor() as cur:
        cur.execute("select * from vw_stock_summary")
        stock_summary = cur.fetchone()
        colnames = [d.name for d in cur.description]
        print('vw_stock_summary:')
        pprint(dict(zip(colnames, stock_summary)))

        # Warning rows from `stock` view
        cur.execute("""
            select quantite, seuil_alerte
            from stock
            where quantite = 0 or quantite <= seuil_alerte
            order by quantite asc, seuil_alerte asc
        """)
        rows = cur.fetchall()
        print('\nstock warnings rows (no names available in this DB user):', len(rows))
        for q, s in rows[:50]:
            print(f"quantite={q}\tseuil_alerte={s}")
        if len(rows) > 50:
            print('...')
