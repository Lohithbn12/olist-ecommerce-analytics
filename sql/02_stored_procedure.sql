-- Builds the star schema from staging tables. Re-run with: CALL sp_refresh_marts();
-- NOTE: 02_build_marts.py executes this file as-is. In MySQL Workbench, wrap the
-- CREATE PROCEDURE with DELIMITER $$ ... END$$ DELIMITER ; before running.
DROP PROCEDURE IF EXISTS sp_refresh_marts;

CREATE PROCEDURE sp_refresh_marts()
BEGIN
    DROP TABLE IF EXISTS fact_orders;
    DROP TABLE IF EXISTS fact_order_items;
    DROP TABLE IF EXISTS dim_product;
    DROP TABLE IF EXISTS dim_seller;
    DROP TABLE IF EXISTS dim_customer;

    -- Order-level fact (one row per order)
    CREATE TABLE fact_orders AS
    SELECT o.order_id,
           c.customer_unique_id,
           o.order_status,
           DATE(o.order_purchase_timestamp) AS order_date,
           o.order_delivered_customer_date  AS delivered_date,
           o.order_estimated_delivery_date  AS estimated_date,
           DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)      AS delivery_days,
           DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) AS delay_days,
           p.payment_value, p.payment_type, r.review_score
    FROM stg_orders o
    JOIN stg_customers c ON c.customer_id = o.customer_id
    LEFT JOIN (
        SELECT order_id, SUM(payment_value) AS payment_value,
               SUBSTRING_INDEX(GROUP_CONCAT(payment_type ORDER BY payment_value DESC), ',', 1) AS payment_type
        FROM stg_payments GROUP BY order_id) p ON p.order_id = o.order_id
    LEFT JOIN (
        SELECT order_id, AVG(review_score) AS review_score
        FROM stg_reviews GROUP BY order_id) r ON r.order_id = o.order_id;

    -- Item-level fact (one row per item, excludes canceled orders)
    CREATE TABLE fact_order_items AS
    SELECT oi.order_id, oi.order_item_id, oi.product_id, oi.seller_id,
           oi.price, oi.freight_value
    FROM stg_order_items oi
    JOIN stg_orders o ON o.order_id = oi.order_id
    WHERE o.order_status <> 'canceled';

    CREATE TABLE dim_product AS
    SELECT p.product_id,
           COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
           p.product_weight_g, p.product_photos_qty
    FROM stg_products p
    LEFT JOIN stg_category_translation t ON t.product_category_name = p.product_category_name;

    CREATE TABLE dim_seller AS
    SELECT seller_id, seller_city, seller_state FROM stg_sellers;

    CREATE TABLE dim_customer AS
    SELECT customer_unique_id,
           MAX(customer_city)  AS city,
           MAX(customer_state) AS state
    FROM stg_customers GROUP BY customer_unique_id;

    CREATE INDEX ix_fo_oid  ON fact_orders (order_id);
    CREATE INDEX ix_fo_cust ON fact_orders (customer_unique_id);
    CREATE INDEX ix_foi_oid ON fact_order_items (order_id);
END
