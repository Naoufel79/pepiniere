import psycopg

conninfo = "postgresql://postgres:KsgyhdFJGPsfBUHTFRsgRUcHfWmYEvzj@interchange.proxy.rlwy.net:44776/railway"

with psycopg.connect(conninfo, connect_timeout=15) as con:
    with con.cursor() as cur:
        cur.execute("""
            select product_id, product_name, quantite, seuil_alerte, is_warning
            from public.v_stock
            order by product_name asc
        """)
        rows = cur.fetchall()

print('count', len(rows))
for pid, name, qty, seuil, warn in rows:
    status = 'WARNING' if warn else 'OK'
    print(f"{pid}\t{status}\t{name}\tqty={qty}\tseuil={seuil}")
