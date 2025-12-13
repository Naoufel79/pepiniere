-- External System Database Views Setup
-- Creates secure views and read-only user for external reporting system
-- Compatible with Django + Railway + PostgreSQL

-- =========================================
-- STEP 1: DISCOVER DJANGO TABLE NAMES
-- =========================================

-- Run this query first to see actual table names:
-- SELECT table_name
-- FROM information_schema.tables
-- WHERE table_schema='public'
--   AND table_name LIKE 'siliana_%'
-- ORDER BY table_name;

-- Expected Django table names (verify with above query):
-- siliana_produit
-- siliana_achat
-- siliana_vente
-- siliana_order
-- siliana_orderitem

-- =========================================
-- STEP 2: CREATE SECURE VIEWS FOR EXTERNAL SYSTEM
-- =========================================

-- Sales View (Ventes)
CREATE OR REPLACE VIEW v_sales AS
SELECT
    id,
    produit_id,
    quantite,
    date_vente,
    quantite * (SELECT prix_vente FROM "Siliana_produit" WHERE id = "Siliana_vente".produit_id) as total_amount
FROM "Siliana_vente"
ORDER BY date_vente DESC;

-- Stock/Products View
CREATE OR REPLACE VIEW v_stock AS
SELECT
    id,
    nom as product_name,
    quantite as current_stock,
    prix_achat as purchase_price,
    prix_vente as selling_price,
    description,
    CASE WHEN quantite > 0 THEN 'available' ELSE 'out_of_stock' END as status,
    (prix_vente - prix_achat) as profit_margin
FROM "Siliana_produit"
ORDER BY nom;

-- Finance Summary View (combines sales and purchases)
CREATE OR REPLACE VIEW v_finance AS
SELECT
    'sale' as transaction_type,
    date_vente as transaction_date,
    quantite * (SELECT prix_vente FROM "Siliana_produit" WHERE id = "Siliana_vente".produit_id) as amount,
    quantite * (SELECT prix_vente - prix_achat FROM "Siliana_produit" WHERE id = "Siliana_vente".produit_id) as profit
FROM "Siliana_vente"
UNION ALL
SELECT
    'purchase' as transaction_type,
    date_achat as transaction_date,
    quantite * (SELECT prix_achat FROM "Siliana_produit" WHERE id = "Siliana_achat".produit_id) as amount,
    0 as profit
FROM "Siliana_achat"
ORDER BY transaction_date DESC;

-- Orders View
CREATE OR REPLACE VIEW v_orders AS
SELECT
    id,
    nom as customer_name,
    telephone as phone,
    wilaya as state,
    ville as city,
    email,
    status,
    date_commande as order_date,
    notes
FROM "Siliana_order"
ORDER BY date_commande DESC;

-- Order Items View
CREATE OR REPLACE VIEW v_order_items AS
SELECT
    oi.id,
    oi.order_id,
    oi.produit_id,
    p.nom as product_name,
    oi.quantite as quantity,
    oi.prix as unit_price,
    (oi.quantite * oi.prix) as total_amount
FROM "Siliana_orderitem" oi
JOIN "Siliana_produit" p ON oi.produit_id = p.id
ORDER BY oi.order_id, oi.id;

-- Dashboard View (Today)
CREATE OR REPLACE VIEW v_dashboard_today AS
SELECT
  (SELECT COUNT(*) FROM "Siliana_produit") AS total_products,
  (SELECT COUNT(*) FROM "Siliana_vente" WHERE date_vente = CURRENT_DATE) AS sales_today,
  (
    SELECT COALESCE(SUM(v.quantite * p.prix_vente), 0)
    FROM "Siliana_vente" v
    JOIN "Siliana_produit" p ON p.id = v.produit_id
    WHERE v.date_vente = CURRENT_DATE
  ) AS revenue_today,
  (SELECT COUNT(*) FROM "Siliana_produit" WHERE quantite <= 5) AS low_stock_count;

-- Sales Summary View - Always returns at least one row with guaranteed non-NULL values
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

-- Stock Summary View - Always returns at least one row with guaranteed non-NULL values
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

-- Finance Summary View - Always returns at least one row with guaranteed non-NULL values
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
-- STEP 3: CREATE READ-ONLY USER WITH LIMITED ACCESS
-- =========================================

-- Create the user
CREATE USER external_client WITH PASSWORD 'Ext3rn4lCl13nt!2025$';

-- Grant basic database access
GRANT CONNECT ON DATABASE railway TO external_client;
GRANT USAGE ON SCHEMA public TO external_client;

-- REVOKE all permissions on schema (be explicit about security)
REVOKE CREATE ON SCHEMA public FROM external_client;
REVOKE USAGE ON SCHEMA public FROM external_client;

-- Grant USAGE back only for the views we created
GRANT USAGE ON SCHEMA public TO external_client;

-- Grant SELECT ONLY on our custom views
GRANT SELECT ON v_sales TO external_client;
GRANT SELECT ON v_stock TO external_client;
GRANT SELECT ON v_finance TO external_client;
GRANT SELECT ON v_orders TO external_client;
GRANT SELECT ON v_order_items TO external_client;
GRANT SELECT ON v_dashboard_today TO external_client;
GRANT SELECT ON v_sales_summary TO external_client;
GRANT SELECT ON v_stock_summary TO external_client;
GRANT SELECT ON v_finance_summary TO external_client;
GRANT SELECT ON vw_sales_summary TO external_client;
GRANT SELECT ON vw_stock_summary TO external_client;
GRANT SELECT ON vw_finance_summary TO external_client;

-- DO NOT grant access to any Django tables
-- DO NOT grant access to auth tables
-- This user can ONLY see the views above

-- =========================================
-- STEP 4: VERIFICATION QUERIES
-- =========================================

-- Check user was created:
-- SELECT usename FROM pg_user WHERE usename = 'external_client';

-- Check view permissions:
-- SELECT grantee, privilege_type, table_name
-- FROM information_schema.role_table_grants
-- WHERE grantee = 'external_client' AND table_name LIKE 'v_%';

-- Test view access (should work):
-- SELECT COUNT(*) FROM v_sales;
-- SELECT COUNT(*) FROM v_stock;

-- Test table access (should FAIL):
-- SELECT COUNT(*) FROM siliana_produit; -- Should be permission denied

-- =========================================
-- STEP 5: EXTERNAL SYSTEM CONNECTION STRING
-- =========================================

-- Railway Public Connection Details:
-- Host: interchange.proxy.rlwy.net
-- Port: 44776
-- Database: railway
-- Username: external_client
-- Password: Ext3rn4lCl13nt!2025$

-- Complete Connection String:
-- postgresql://external_client:Ext3rn4lCl13nt!2025$@interchange.proxy.rlwy.net:44776/railway

-- =========================================
-- CLEANUP (if needed)
-- =========================================

-- To drop everything (CAUTION - only if needed):
-- DROP VIEW IF EXISTS v_sales, v_stock, v_finance, v_orders, v_order_items, v_dashboard_today, v_sales_summary, v_stock_summary, v_finance_summary, vw_sales_summary, vw_stock_summary, vw_finance_summary;
-- DROP USER IF EXISTS external_client;

-- =========================================
-- ADDITIONAL SECURITY NOTES
-- =========================================

-- 1. Change the password regularly
-- 2. Monitor access logs
-- 3. Never give this user access to Django's auth tables
-- 4. Views hide sensitive internal data
-- 5. External system can only read aggregated/reporting data
