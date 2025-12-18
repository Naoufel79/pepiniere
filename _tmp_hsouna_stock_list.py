import psycopg

conninfo = "postgresql://postgres:KsgyhdFJGPsfBUHTFRsgRUcHfWmYEvzj@interchange.proxy.rlwy.net:44776/railway"

with psycopg.connect(conninfo, connect_timeout=15) as con:
    with con.cursor() as cur:
        # Core list with threshold logic (same as required_views.sql)
        cur.execute("""
            select
              p.id,
              p.nom as product_name,
              p.quantite,
              case when p.quantite <= 5 then 5 else 10 end as seuil_alerte,
              case
                when p.quantite = 0 then 'rupture'
                when p.quantite <= (case when p.quantite <= 5 then 5 else 10 end) then 'alerte'
                else 'ok'
              end as statut
            from "Siliana_produit" p
            where p.quantite = 0
               or p.quantite <= (case when p.quantite <= 5 then 5 else 10 end)
            order by p.quantite asc, p.nom asc
        """)
        rows = cur.fetchall()

print('count', len(rows))
for (pid, name, qty, seuil, statut) in rows:
    print(f"{statut}\t{name}\tqty={qty}\tseuil={seuil}\tid={pid}")
