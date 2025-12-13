-- Test User Setup for External System Connection Testing
-- Creates a temporary user with simple ASCII password for debugging
-- PostgreSQL + Railway compatible

-- =========================================
-- CREATE TEST USER WITH SIMPLE PASSWORD
-- =========================================

-- Create user with simple password (ASCII only, no special chars)
CREATE USER client_test WITH PASSWORD 'Test12345';

-- Grant basic database access
GRANT CONNECT ON DATABASE railway TO client_test;
GRANT USAGE ON SCHEMA public TO client_test;

-- Grant SELECT on ALL tables for testing (temporary)
GRANT SELECT ON ALL TABLES IN SCHEMA public TO client_test;

-- Grant SELECT on sequences (for completeness)
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO client_test;

-- =========================================
-- CONNECTION TEST DETAILS
-- =========================================

-- Railway Public Connection Details for Testing:
-- Host: interchange.proxy.rlwy.net
-- Port: 44776
-- Database: railway
-- Username: client_test
-- Password: Test12345
-- DB Type: PostgreSQL

-- Connection String:
-- postgresql://client_test:Test12345@interchange.proxy.rlwy.net:44776/railway

-- =========================================
-- VERIFICATION QUERIES
-- =========================================

-- Check user was created:
-- SELECT usename FROM pg_user WHERE usename = 'client_test';

-- Test connection (should work):
-- SELECT COUNT(*) FROM siliana_produit;

-- =========================================
-- CLEANUP AFTER TESTING
-- =========================================

-- After testing, remove the test user:
-- DROP USER IF EXISTS client_test;

-- =========================================
-- EXPECTED BEHAVIOR
-- =========================================

-- If connection succeeds with this simple password:
-- → Issue is in external system's password handling/encryption
-- → External system needs to fix credential processing

-- If connection still fails:
-- → Issue is elsewhere (network, PostgreSQL config, etc.)
-- → Investigate Railway/firewall/network issues
