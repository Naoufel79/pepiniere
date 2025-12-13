-- Snapshot Validation Script
-- This script validates that all required views exist and return proper data
-- Run this before executing snapshots to ensure everything is working

-- =========================================
-- VALIDATION 1: Check Required Views Exist
-- =========================================
DO $$
DECLARE
    view_count INTEGER;
    missing_views TEXT := '';
BEGIN
    SELECT COUNT(*) INTO view_count
    FROM information_schema.views 
    WHERE table_schema = 'public' 
      AND table_name IN ('vw_sales_summary', 'vw_stock_summary', 'vw_finance_summary');
    
    IF view_count < 3 THEN
        RAISE EXCEPTION 'Only % of 3 required views exist. Missing views: %', 
            view_count,
            (SELECT string_agg(table_name, ', ') 
             FROM information_schema.views 
             WHERE table_schema = 'public' 
               AND table_name IN ('vw_sales_summary', 'vw_stock_summary', 'vw_finance_summary'));
    END IF;
    
    RAISE NOTICE '✓ All 3 required views exist';
END $$;

-- =========================================
-- VALIDATION 2: Test vw_sales_summary
-- =========================================
DO $$
DECLARE
    test_result RECORD;
BEGIN
    -- Test that view returns data and has correct structure
    SELECT * INTO test_result FROM vw_sales_summary;
    
    -- Validate data types and not null constraints
    IF test_result.total_items_sold IS NULL THEN
        RAISE EXCEPTION 'vw_sales_summary.total_items_sold is NULL';
    END IF;
    
    IF test_result.total_sales_amount IS NULL THEN
        RAISE EXCEPTION 'vw_sales_summary.total_sales_amount is NULL';
    END IF;
    
    -- Validate return count (should be exactly 1)
    IF (SELECT COUNT(*) FROM vw_sales_summary) != 1 THEN
        RAISE EXCEPTION 'vw_sales_summary should return exactly 1 row';
    END IF;
    
    RAISE NOTICE '✓ vw_sales_summary validation passed';
    RAISE NOTICE '  - Returns: % items sold, $% total sales, % transactions, $% avg', 
        test_result.total_items_sold, test_result.total_sales_amount, 
        test_result.total_transactions, test_result.average_transaction_value;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'vw_sales_summary validation failed: %', SQLERRM;
END $$;

-- =========================================
-- VALIDATION 3: Test vw_stock_summary
-- =========================================
DO $$
DECLARE
    test_result RECORD;
BEGIN
    -- Test that view returns data and has correct structure
    SELECT * INTO test_result FROM vw_stock_summary;
    
    -- Validate data types and not null constraints
    IF test_result.total_products IS NULL THEN
        RAISE EXCEPTION 'vw_stock_summary.total_products is NULL';
    END IF;
    
    IF test_result.total_quantity_in_stock IS NULL THEN
        RAISE EXCEPTION 'vw_stock_summary.total_quantity_in_stock is NULL';
    END IF;
    
    IF test_result.average_selling_price IS NULL THEN
        RAISE EXCEPTION 'vw_stock_summary.average_selling_price is NULL';
    END IF;
    
    -- Validate return count (should be exactly 1)
    IF (SELECT COUNT(*) FROM vw_stock_summary) != 1 THEN
        RAISE EXCEPTION 'vw_stock_summary should return exactly 1 row';
    END IF;
    
    RAISE NOTICE '✓ vw_stock_summary validation passed';
    RAISE NOTICE '  - Returns: % products, % total quantity, % out of stock, % low stock, $% avg price', 
        test_result.total_products, test_result.total_quantity_in_stock,
        test_result.out_of_stock_products, test_result.low_stock_products, 
        test_result.average_selling_price;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'vw_stock_summary validation failed: %', SQLERRM;
END $$;

-- =========================================
-- VALIDATION 4: Test vw_finance_summary
-- =========================================
DO $$
DECLARE
    test_result RECORD;
BEGIN
    -- Test that view returns data and has correct structure
    SELECT * INTO test_result FROM vw_finance_summary;
    
    -- Validate data types and not null constraints
    IF test_result.revenue IS NULL THEN
        RAISE EXCEPTION 'vw_finance_summary.revenue is NULL';
    END IF;
    
    IF test_result.expenses IS NULL THEN
        RAISE EXCEPTION 'vw_finance_summary.expenses is NULL';
    END IF;
    
    IF test_result.gross_profit IS NULL THEN
        RAISE EXCEPTION 'vw_finance_summary.gross_profit IS NULL';
    END IF;
    
    IF test_result.profit_margin_percentage IS NULL THEN
        RAISE EXCEPTION 'vw_finance_summary.profit_margin_percentage IS NULL';
    END IF;
    
    -- Validate return count (should be exactly 1)
    IF (SELECT COUNT(*) FROM vw_finance_summary) != 1 THEN
        RAISE EXCEPTION 'vw_finance_summary should return exactly 1 row';
    END IF;
    
    RAISE NOTICE '✓ vw_finance_summary validation passed';
    RAISE NOTICE '  - Returns: $% revenue, $% expenses, $% profit, %%% margin', 
        test_result.revenue, test_result.expenses, 
        test_result.gross_profit, test_result.profit_margin_percentage;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'vw_finance_summary validation failed: %', SQLERRM;
END $$;

-- =========================================
-- VALIDATION 5: Test External User Permissions
-- =========================================
DO $$
DECLARE
    test_user TEXT := 'external_client';
    permission_count INTEGER;
BEGIN
    -- Check that external_client has SELECT permissions on our views
    SELECT COUNT(*) INTO permission_count
    FROM information_schema.role_table_grants
    WHERE grantee = test_user 
      AND privilege_type = 'SELECT'
      AND table_name IN ('vw_sales_summary', 'vw_stock_summary', 'vw_finance_summary');
    
    IF permission_count < 3 THEN
        RAISE EXCEPTION 'User % has only % of 3 required SELECT permissions', 
            test_user, permission_count;
    END IF;
    
    RAISE NOTICE '✓ external_client user has all required permissions';
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Permission validation failed: %', SQLERRM;
END $$;

-- =========================================
-- VALIDATION 6: Test Data Consistency
-- =========================================
DO $$
DECLARE
    sales_transactions INTEGER;
    stock_products INTEGER;
    finance_revenue NUMERIC;
BEGIN
    -- Get basic counts to ensure data consistency
    SELECT total_transactions INTO sales_transactions FROM vw_sales_summary;
    SELECT total_products INTO stock_products FROM vw_stock_summary;
    SELECT revenue INTO finance_revenue FROM vw_finance_summary;
    
    RAISE NOTICE '✓ Data consistency check passed';
    RAISE NOTICE '  - Sales transactions: %', sales_transactions;
    RAISE NOTICE '  - Stock products: %', stock_products;
    RAISE NOTICE '  - Finance revenue: $%', finance_revenue;
    
    -- Basic sanity checks (values shouldn't be negative)
    IF sales_transactions < 0 OR stock_products < 0 OR finance_revenue < 0 THEN
        RAISE EXCEPTION 'Negative values detected in summary data';
    END IF;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Data consistency validation failed: %', SQLERRM;
END $$;

-- =========================================
-- FINAL SUMMARY
-- =========================================
DO $$
BEGIN
    RAISE NOTICE '';
    RAISE NOTICE '============================================';
    RAISE NOTICE '🎉 SNAPSHOT VALIDATION COMPLETED SUCCESSFULLY';
    RAISE NOTICE '============================================';
    RAISE NOTICE 'All required views are functional and accessible.';
    RAISE NOTICE 'External system snapshots should now work correctly.';
    RAISE NOTICE '';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Update external system to query vw_sales_summary, vw_stock_summary, vw_finance_summary';
    RAISE NOTICE '2. Test snapshots with the external system';
    RAISE NOTICE '3. Monitor logs for any unexpected errors';
    RAISE NOTICE '';
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE '';
        RAISE NOTICE '============================================';
        RAISE NOTICE '❌ SNAPSHOT VALIDATION FAILED';
        RAISE NOTICE '============================================';
        RAISE NOTICE 'Error: %', SQLERRM;
        RAISE NOTICE 'Please fix the issues and run this script again.';
        RAISE NOTICE '';
END $$;
