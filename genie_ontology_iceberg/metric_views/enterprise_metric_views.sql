-- ============================================================================
-- Databricks Unity Catalog Metric Views
-- Standardizes enterprise definitions across Genie, AI/BI, Dashboards, and Agents
-- ============================================================================

-- 1. Financial Revenue & Churn Metric View
CREATE OR REPLACE VIEW gold.finance.metric_revenue_and_churn
AS
SELECT
    DATE_TRUNC('month', t.transaction_date) AS fiscal_month,
    t.product_line,
    c.segment,
    c.country_code,
    -- Measures
    SUM(t.net_amount) AS total_revenue,
    SUM(CASE WHEN t.transaction_type = 'RECURRING' THEN t.net_amount ELSE 0.0 END) AS arr,
    SUM(t.cost_of_goods_sold) AS total_cogs,
    (SUM(t.net_amount) - SUM(t.cost_of_goods_sold)) / NULLIF(SUM(t.net_amount), 0.0) AS gross_margin_pct,
    COUNT(DISTINCT t.customer_id) AS active_subscribers,
    AVG(c.churn_risk_score) AS avg_churn_risk
FROM gold.finance.fact_transactions t
INNER JOIN gold.enterprise.customer_master c
    ON t.customer_id = c.customer_id
WHERE t.status = 'SETTLED'
  AND t.is_test_record = FALSE
GROUP BY 1, 2, 3, 4;

-- Certify Metric View in Unity Catalog
ALTER VIEW gold.finance.metric_revenue_and_churn
SET TAGS (
    'governance_tier' = 'certified_gold',
    'semantic_type' = 'metric_view',
    'owner' = 'dana.whitlock@company.com',
    'domain' = 'Finance'
);

-- 2. Sales Pipeline & Customer Expansion Metric View
CREATE OR REPLACE VIEW gold.sales.metric_customer_expansion
AS
SELECT
    c.customer_id,
    c.customer_name,
    c.segment,
    c.country_code,
    c.lifetime_value,
    COALESCE(SUM(t.net_amount), 0.0) AS trailing_30d_consumption,
    CASE 
        WHEN COALESCE(SUM(t.net_amount), 0.0) > 10000.0 THEN 'HIGH_EXPANSION'
        WHEN COALESCE(SUM(t.net_amount), 0.0) > 2000.0 THEN 'STEADY_EXPANSION'
        ELSE 'MAINTAIN'
    END AS expansion_category
FROM gold.enterprise.customer_master c
LEFT JOIN gold.finance.fact_transactions t
    ON c.customer_id = t.customer_id
   AND t.transaction_date >= CURRENT_DATE() - INTERVAL 30 DAYS
   AND t.is_test_record = FALSE
GROUP BY 1, 2, 3, 4, 5;

ALTER VIEW gold.sales.metric_customer_expansion
SET TAGS (
    'governance_tier' = 'certified_gold',
    'semantic_type' = 'metric_view',
    'owner' = 'chung.wu@company.com',
    'domain' = 'Sales'
);
