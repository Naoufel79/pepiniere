# External System Documentation - PostgreSQL Views

## Overview

This documentation provides the external system with stable, guaranteed endpoints for querying business KPIs through PostgreSQL views. The views act as a compatibility layer, ensuring consistent data access regardless of internal database schema changes.

## Connection Details

```
Host: interchange.proxy.rlwy.net
Port: 44776
Database: railway
Username: external_client
Password: Ext3rn4lCl13nt!2025$
```

**Connection String:** `postgresql://external_client:Ext3rn4lCl13nt!2025$@interchange.proxy.rlwy.net:44776/railway`

## Core KPI Views

### 1. Sales Summary (`vw_sales_summary`)

**Purpose:** Provides comprehensive sales metrics with guaranteed data availability.

**Query:**
```sql
SELECT * FROM vw_sales_summary;
```

**Response Schema:**
```json
{
  "total_items_sold": "INTEGER",
  "total_sales_amount": "NUMERIC(15,2)",
  "total_transactions": "INTEGER", 
  "average_transaction_value": "NUMERIC(15,2)"
}
```

**Behavior:**
- Always returns exactly one row
- Never returns NULL values (uses COALESCE)
- If no sales data exists, returns: `0, 0.00, 0, 0.00`
- Data types are explicitly cast for stability

### 2. Stock Summary (`vw_stock_summary`)

**Purpose:** Provides inventory metrics with guaranteed data availability.

**Query:**
```sql
SELECT * FROM vw_stock_summary;
```

**Response Schema:**
```json
{
  "total_products": "INTEGER",
  "total_quantity_in_stock": "INTEGER",
  "out_of_stock_products": "INTEGER",
  "low_stock_products": "INTEGER",
  "average_selling_price": "NUMERIC(15,2)"
}
```

**Behavior:**
- Always returns exactly one row
- Never returns NULL values (uses COALESCE)
- If no products exist, returns: `0, 0, 0, 0, 0.00`
- Low stock threshold: products with 1-5 units remaining

### 3. Finance Summary (`vw_finance_summary`)

**Purpose:** Provides financial metrics combining sales and purchases with guaranteed data availability.

**Query:**
```sql
SELECT * FROM vw_finance_summary;
```

**Response Schema:**
```json
{
  "revenue": "NUMERIC(15,2)",
  "expenses": "NUMERIC(15,2)",
  "gross_profit": "NUMERIC(15,2)",
  "profit_margin_percentage": "NUMERIC(5,2)"
}
```

**Behavior:**
- Always returns exactly one row
- Never returns NULL values (uses COALESCE)
- If no transactions exist, returns: `0.00, 0.00, 0.00, 0.00`
- Revenue = total sales amount
- Expenses = total purchases amount
- Gross profit = revenue - cost of goods sold
- Profit margin = (revenue / expenses) * 100 when expenses > 0, else 0

## Snapshot Execution Logic

### Pre-Validation Step

Before executing snapshots, perform this validation:

```sql
-- Check if required views exist
SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public' 
  AND table_name IN ('vw_sales_summary', 'vw_stock_summary', 'vw_finance_summary')
ORDER BY table_name;
```

**Expected Result:** 3 rows (one for each view)

### Snapshot Query Pattern

```python
# Python-like pseudocode
def execute_snapshot():
    try:
        # 1. Sales Data
        sales_data = query_database("SELECT * FROM vw_sales_summary")
        if not sales_data:
            log_error("vw_sales_summary returned no data")
            return {"error": "No sales data available"}
        
        # 2. Stock Data  
        stock_data = query_database("SELECT * FROM vw_stock_summary")
        if not stock_data:
            log_error("vw_stock_summary returned no data")
            return {"error": "No stock data available"}
        
        # 3. Finance Data
        finance_data = query_database("SELECT * FROM vw_finance_summary")
        if not finance_data:
            log_error("vw_finance_summary returned no data")
            return {"error": "No finance data available"}
        
        # 4. Build snapshot result
        return {
            "sales": sales_data[0],  # Always exists due to UNION ALL
            "stock": stock_data[0],  # Always exists due to UNION ALL  
            "finance": finance_data[0]  # Always exists due to UNION ALL
        }
        
    except Exception as e:
        log_error(f"Snapshot failed: {str(e)}")
        return {"error": f"Snapshot execution failed: {str(e)}"}
```

### Error Handling

**Clear Error Messages:**
- "View 'vw_sales_summary' does not exist" → Database setup incomplete
- "vw_sales_summary returned no data" → Should never happen (fallback UNION ALL ensures data)
- Connection errors → Network/credentials issues
- Permission denied → User access problems

**Log Examples:**
```
[INFO] Validation passed: All 3 required views exist
[INFO] Snapshot executed successfully: Sales=1250.00, Stock=45 products, Finance=15.2% margin
[WARN] vw_sales_summary returned zero values (expected for new database)
[ERROR] Connection failed: invalid password
[ERROR] View 'vw_sales_summary' missing - run database setup script
```

## Testing Commands

### 1. Connection Test
```bash
psql "postgresql://external_client:Ext3rn4lCl13nt!2025$@interchange.proxy.rlwy.net:44776/railway" -c "SELECT version();"
```

### 2. View Accessibility Test
```sql
-- Should work (returns data)
SELECT * FROM vw_sales_summary;
SELECT * FROM vw_stock_summary; 
SELECT * FROM vw_finance_summary;

-- Should fail (no direct table access)
SELECT * FROM siliana_produit; -- ERROR: permission denied
```

### 3. Data Validation Test
```sql
-- Verify data types and non-NULL guarantees
SELECT 
  pg_typeof(total_items_sold) as sales_type,
  pg_typeof(total_sales_amount) as amount_type,
  total_items_sold IS NOT NULL as sales_not_null,
  total_sales_amount IS NOT NULL as amount_not_null
FROM vw_sales_summary 
LIMIT 1;
```

## Migration Guide

### Updating External System

1. **Replace old table queries with view queries:**
   ```sql
   -- OLD (unreliable)
   SELECT COUNT(*) FROM siliana_produit;
   
   -- NEW (guaranteed)
   SELECT * FROM vw_stock_summary;
   ```

2. **Update error handling:**
   ```javascript
   // OLD
   if (result === '{}') {
     // Silent failure
   }
   
   // NEW  
   if (result.error) {
     console.error('Snapshot failed:', result.error);
   }
   ```

3. **Test with empty database:**
   - Create fresh test database
   - Run external_system_views_setup.sql
   - Execute queries - should return zero values, not errors

## Compatibility Guarantees

✅ **Column Names:** Stable and version-controlled
✅ **Data Types:** Explicitly cast (INTEGER, NUMERIC(15,2), etc.)
✅ **Null Safety:** All numeric fields use COALESCE
✅ **Row Count:** Always returns exactly one row per view
✅ **Schema Independence:** Views hide internal table structure
✅ **Performance:** Optimized with LEFT JOINs and subqueries
✅ **Scalability:** Efficient for large datasets

## Support

For issues:
1. Verify database setup: `external_system_views_setup.sql`
2. Check view existence: `information_schema.views`
3. Test connection and permissions
4. Validate data types and null handling
5. Review error logs for specific failure points

**Never modify internal Django tables - use views only.**
