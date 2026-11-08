SELECT COUNT(*) AS rows_fact_orders FROM fact_orders;                -- ~99,441
SELECT COUNT(DISTINCT order_id) AS distinct_orders FROM fact_orders; -- must equal above
SELECT ROUND(SUM(price)) AS total_revenue FROM fact_order_items;     -- ~13.5M
SELECT order_status, COUNT(*) FROM fact_orders GROUP BY order_status;
