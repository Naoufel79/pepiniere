import psycopg

# NOTE: credentials provided by user; do not print conninfo.
conninfo = "postgresql://postgres:KsgyhdFJGPsfBUHTFRsgRUcHfWmYEvzj@interchange.proxy.rlwy.net:44776/railway"

create_view_sql = """
CREATE OR REPLACE VIEW public.v_stock AS
SELECT
  id AS product_id,
  nom AS product_name,
  quantite,
  CASE WHEN quantite <= 5 THEN 5 ELSE 10 END AS seuil_alerte,
  (quantite = 0 OR quantite <= CASE WHEN quantite <= 5 THEN 5 ELSE 10 END) AS is_warning
FROM public."Siliana_produit";
"""

grant_sql = "GRANT SELECT ON public.v_stock TO external_client;"

with psycopg.connect(conninfo, connect_timeout=15) as con:
    con.execute(create_view_sql)
    con.commit()

    grant_ok = True
    try:
        con.execute(grant_sql)
        con.commit()
    except Exception as e:
        con.rollback()
        grant_ok = False
        grant_err = str(e)

    # Verify view shape + sample warnings
    with con.cursor() as cur:
        cur.execute("""
            select column_name, data_type
            from information_schema.columns
            where table_schema='public' and table_name='v_stock'
            order by ordinal_position
        """)
        cols = cur.fetchall()

        cur.execute("""
            select product_id, product_name, quantite, seuil_alerte, is_warning
            from public.v_stock
            where is_warning
            order by quantite asc, product_name asc
        """)
        warning_rows = cur.fetchall()

print('v_stock created/updated: OK')
print('columns:')
for c in cols:
    print(' -', c[0], c[1])
print('warnings:', len(warning_rows))
for r in warning_rows[:50]:
    pid, name, qty, seuil, is_warn = r
    print(f" - {name} (id={pid}) qty={qty} seuil={seuil} is_warning={is_warn}")
if not grant_ok:
    print('\nGRANT failed (role may not exist or permissions issue):')
    print(grant_err)
else:
    print('\nGRANT SELECT to external_client: OK')
