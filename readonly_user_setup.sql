-- PostgreSQL Read-Only User Setup Script
-- Creates a user with SELECT-only permissions
-- Compatible with PostgreSQL 14+

-- Connect to your database first, then run this script
-- Replace 'your_database_name' with your actual database name

-- 1. Create the read-only user
CREATE USER client_readonly WITH PASSWORD 'secure_password_here';

-- 2. Grant CONNECT privilege to the database
-- Replace 'your_database_name' with your actual database name
GRANT CONNECT ON DATABASE your_database_name TO client_readonly;

-- 3. Grant USAGE on schema (allows access to schema objects)
GRANT USAGE ON SCHEMA public TO client_readonly;

-- 4. Grant SELECT privilege on ALL existing tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO client_readonly;

-- 5. Grant SELECT privilege on ALL future tables (created after this script)
-- This ensures future tables are automatically accessible to the read-only user
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO client_readonly;

-- 6. Grant SELECT on sequences (for SERIAL/auto-incrementing columns)
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO client_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON SEQUENCES TO client_readonly;

-- 7. Optional: Grant EXECUTE on functions (if your app uses custom functions)
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO client_readonly;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO client_readonly;

-- Verification queries (run these separately to check permissions):

-- Check user exists:
-- SELECT usename FROM pg_user WHERE usename = 'client_readonly';

-- Check database privileges:
-- SELECT grantee, privilege_type FROM information_schema.role_table_grants
-- WHERE grantee = 'client_readonly';

-- Test connection (from another session):
-- psql -h your_host -p your_port -U client_readonly -d your_database_name

-- Note: The user will only be able to run SELECT queries
-- All INSERT, UPDATE, DELETE operations will be denied
