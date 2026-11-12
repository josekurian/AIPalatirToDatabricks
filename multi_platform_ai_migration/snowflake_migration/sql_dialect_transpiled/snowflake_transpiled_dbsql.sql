-- ==============================================================================
-- Snowflake SQL Dialect to Databricks SQL Transpiled Queries
-- Refactors Snowflake proprietary functions (ZEROIFNULL, IFF, DATEADD, FLATTEN)
-- into high-performance ANSI Databricks SQL powered by the Photon C++ engine.
-- ==============================================================================

-- 1. Transpiled Dimensional Sales Metrics View
CREATE OR REPLACE VIEW enterprise_operations.gold.v_transpiled_snowflake_sales AS
SELECT 
    order_id,
    customer_id,
    -- Snowflake ZEROIFNULL(discount_amount) -> COALESCE(discount_amount, 0.0)
    COALESCE(discount_amount, 0.0) AS discount_amount_clean,
    
    -- Snowflake IFF(order_total > 100000, 'KEY_ACCOUNT', 'STANDARD') -> CASE WHEN
    CASE 
        WHEN order_total_usd >= 100000.0 THEN 'KEY_ACCOUNT' 
        ELSE 'STANDARD' 
    END AS account_tier,
    
    -- Snowflake DATEADD(day, 30, order_date) -> DATE_ADD(order_date, 30)
    DATE_ADD(order_date, 30) AS payment_due_date,
    
    -- Net Sales calculation
    (order_total_usd - COALESCE(discount_amount, 0.0)) AS net_sales_usd
FROM enterprise_operations.gold.fact_supply_order;

-- 2. Semi-Structured JSON Parsing (Snowflake FLATTEN -> Databricks EXPLODE)
CREATE OR REPLACE VIEW enterprise_operations.gold.v_transpiled_order_line_items AS
SELECT 
    order_id,
    customer_id,
    line_item.sku_id AS sku_id,
    line_item.quantity AS quantity_ordered,
    line_item.unit_price AS unit_price_usd
FROM enterprise_operations.gold.fact_supply_order,
LATERAL EXPLODE(raw_line_items_array) AS t(line_item);
