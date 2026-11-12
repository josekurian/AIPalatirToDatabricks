# Unity Catalog Page: Consumption Revenue Recognition & ARR
**Namespace**: `gold.finance` | **Status**: Certified Gold | **Domain**: Finance  
**Lead Steward**: Dana Whitlock (Lead Financial Architect) | **Co-Owner**: Chung Wu  
**Telemetry**: Referenced in 26,400+ Genie responses | Quality Rating: 99.4%

---

## 1. Executive Business Definitions
- **ARR (Annual Recurring Revenue)**: Calculated exclusively from contracts where `transaction_type = 'RECURRING'`. Professional services, pilot credits, and ad-hoc migrations are explicitly excluded.
- **Active Paying Customer**: Any account with settled revenue (`status = 'SETTLED'`) within the trailing 30 days.
- **Gross Margin %**: Defined as `(Total Revenue - COGS) / Total Revenue`. Target benchmark is $\ge 78\%$.
- **Fiscal Calendar Alignment**: Fiscal Year begins February 1st. Q1 (Feb-Apr), Q2 (May-Jul), Q3 (Aug-Oct), Q4 (Nov-Jan).

---

## 2. Genie Natural Language Guardrails & Routing Rules
1. **Always Filter Test Records**: Genie MUST include `is_test_record = FALSE` on every query referencing `fact_transactions`.
2. **Default Metric Source**: When the user asks for "Revenue", "ARR", or "Margin", query `gold.finance.metric_revenue_and_churn` rather than raw event streams.
3. **Ambiguity Resolution**: If a user asks for "Top accounts", sort by `trailing_30d_consumption` descending unless specified by lifetime value.

---

## 3. Certified Question-SQL Benchmark Pairs (Few-Shot Evaluation Ground Truth)

### Benchmark 1: Top 5 Customers by Revenue in North America
```sql
SELECT c.customer_name, SUM(t.net_amount) AS total_revenue
FROM gold.finance.fact_transactions t
JOIN gold.enterprise.customer_master c ON t.customer_id = c.customer_id
WHERE c.country_code IN ('US', 'CA')
  AND t.is_test_record = FALSE
  AND t.status = 'SETTLED'
GROUP BY c.customer_name
ORDER BY total_revenue DESC
LIMIT 5;
```

### Benchmark 2: Fiscal Q3 ARR by Product Family
```sql
SELECT product_line, SUM(arr) AS quarterly_arr
FROM gold.finance.metric_revenue_and_churn
WHERE fiscal_month BETWEEN '2026-08-01' AND '2026-10-31'
GROUP BY product_line
ORDER BY quarterly_arr DESC;
```
