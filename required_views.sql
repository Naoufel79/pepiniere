-- Required Views Creation Script
-- Creates 3 views with specific columns as requested

-- =========================================
-- 1. Ventes View
-- =========================================
CREATE OR REPLACE VIEW ventes AS
SELECT
  CAST(v.quantite * p.prix_vente AS NUMERIC(15,2)) AS montant,
  v.date_vente
FROM "Siliana_vente" v
LEFT JOIN "Siliana_produit" p ON p.id = v.produit_id;

-- =============********============================
-- 2. Stock View  
-- =========================================
CREATE OR REPLACE VIEW stock AS
SELECT
  p.quantite,
  CASE 
    WHEN p.quantite <= 5 THEN 5
    ELSE 10 
  END AS seuil_alerte
FROM "Siliana_produit" p;

-- =========================================
-- 3. Transactions Financieres View
-- =========================================
CREATE OR REPLACE VIEW transactions_financieres AS
SELECT
  'vente' as type,
  CAST(v.quantite * p.prix_vente AS NUMERIC(15,2)) as montant,
  v.date_vente as date_transaction
FROM "Siliana_vente" v
LEFT JOIN "Siliana_produit" p ON p.id = v.produit_id

UNION ALL

SELECT
  'achat' as type,
  CAST(a.quantite * p.prix_achat AS NUMERIC(15,2)) as montant,
  a.date_achat as date_transaction
FROM "Siliana_achat" a
LEFT JOIN "Siliana_produit" p ON p.id = a.produit_id;

-- =========================================
-- GRANT PERMISSIONS
-- =========================================
GRANT SELECT ON ventes TO external_client;
GRANT SELECT ON stock TO external_client;
GRANT SELECT ON transactions_financieres TO external_client;

-- =========================================
-- VERIFICATION
-- =========================================
-- Test that all views work correctly
SELECT 'ventes' as view_name, COUNT(*) as row_count FROM ventes;
SELECT 'stock' as view_name, COUNT(*) as row_count FROM stock;
SELECT 'transactions_financieres' as view_name, COUNT(*) as row_count FROM transactions_financieres;

-- Show sample data from each view
SELECT * FROM ventes LIMIT 5;
SELECT * FROM stock LIMIT 5;
SELECT * FROM transactions_financieres LIMIT 5;

-- =========================================
-- VIEW DESCRIPTIONS
-- =========================================
-- 1. ventes: Shows sales amount (montant) and sale date (date_vente)
-- 2. stock: Shows quantity (quantite) and alert threshold (seuil_alerte)
-- 3. transactions_financieres: Shows transaction type, amount and date
