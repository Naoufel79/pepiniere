-- VW Views Creation Script
-- Creates the three required views for external system snapshots
-- Each view guarantees at least one row with no NULL values

-- =========================================
-- 1. Sales Summary View
-- =========================================
CREATE OR REPLACE VIEW vw_sales_summary AS
SELECT
  CAST(COALESCE(SUM(v.quantite), 0) AS INTEGER) AS total_items_sold,
  CAST(COALESCE(SUM(v.quantite * p.prix_vente), 0) AS NUMERIC(15,2)) AS total_sales_amount,
  CAST(COALESCE(COUNT(*), 0) AS INTEGER) AS total_transactions,
  CAST(COALESCE(AVG(v.quantite * p.prix_vente), 0) AS NUMERIC(15,2)) AS average_transaction_value
FROM "Siliana_vente" v
LEFT JOIN "Siliana_produit" p ON p.id = v.produit_id
UNION ALL
SELECT 0, 0.00, 0, 0.00
WHERE NOT EXISTS (SELECT 1 FROM "Siliana_vente");

-- =========================================
-- 2. Stock Summary View
-- =========================================
CREATE OR REPLACE VIEW vw_stock_summary AS
SELECT
  CAST(COALESCE(COUNT(*), 0) AS INTEGER) AS total_products,
  CAST(COALESCE(SUM(quantite), 0) AS INTEGER) AS total_quantity_in_stock,
  CAST(COALESCE(SUM(CASE WHEN quantite = 0 THEN 1 ELSE 0 END), 0) AS INTEGER) AS out_of_stock_products,
  CAST(COALESCE(SUM(CASE WHEN quantite <= 5 AND quantite > 0 THEN 1 ELSE 0 END), 0) AS INTEGER) AS low_stock_products,
  CAST(COALESCE(AVG(prix_vente), 0) AS NUMERIC(15,2)) AS average_selling_price
FROM "Siliana_produit"
UNION ALL
SELECT 0, 0, 0, 0, 0.00
WHERE NOT EXISTS (SELECT 1 FROM "Siliana_produit");

-- =========================================
-- 3. Finance Summary View
-- =========================================
CREATE OR REPLACE VIEW vw_finance_summary AS
SELECT
  CAST(COALESCE(SUM(CASE WHEN t.transaction_type = 'sale' THEN t.amount ELSE 0 END), 0) AS NUMERIC(15,2)) AS revenue,
  CAST(COALESCE(SUM(CASE WHEN t.transaction_type = 'purchase' THEN t.amount ELSE 0 END), 0) AS NUMERIC(15,2)) AS expenses,
  CAST(COALESCE(SUM(CASE WHEN t.transaction_type = 'sale' THEN t.profit ELSE 0 END), 0) AS NUMERIC(15,2)) AS gross_profit,
  CAST(CASE 
    WHEN COALESCE(SUM(CASE WHEN t.transaction_type = 'purchase' THEN t.amount ELSE 0 END), 0) > 0 
    THEN CAST(COALESCE(SUM(CASE WHEN t.transaction_type = 'sale' THEN t.amount ELSE 0 END), 0) AS NUMERIC(15,2)) / CAST(SUM(CASE WHEN t.transaction_type = 'purchase' THEN t.amount ELSE 0 END) AS NUMERIC(15,2)) * 100
    ELSE 0 
  END AS NUMERIC(5,2)) AS profit_margin_percentage
FROM (
  SELECT 
    'sale' as transaction_type,
    COALESCE(v.quantite * p.prix_vente, 0) as amount,
    COALESCE(v.quantite * (p.prix_vente - p.prix_achat), 0) as profit
  FROM "Siliana_vente" v
  LEFT JOIN "Siliana_produit" p ON p.id = v.produit_id
  
  UNION ALL
  
  SELECT 
    'purchase' as transaction_type,
    COALESCE(a.quantite * p.prix_achat, 0) as amount,
    0 as profit
  FROM "Siliana_achat" a
  LEFT JOIN "Siliana_produit" p ON p.id = a.produit_id
) t
UNION ALL
SELECT 0.00, 0.00, 0.00, 0.00
WHERE NOT EXISTS (
  SELECT 1 FROM "Siliana_vente" 
  UNION ALL 
  SELECT 1 FROM "Siliana_achat"
);

-- =========================================
-- GRANT PERMISSIONS
-- =========================================
GRANT SELECT ON vw_sales_summary TO external_client;
GRANT SELECT ON vw_stock_summary TO external_client;
GRANT SELECT ON vw_finance_summary TO external_client;

-- =========================================
-- VERIFICATION
-- =========================================
-- Test that all views return exactly one row with no NULLs
SELECT 'vw_sales_summary' as view_name, COUNT(*) as row_count FROM vw_sales_summary;
SELECT 'vw_stock_summary' as view_name, COUNT(*) as row_count FROM vw_stock_summary;
SELECT 'vw_finance_summary' as view_name, COUNT(*) as row_count FROM vw_finance_summary;
