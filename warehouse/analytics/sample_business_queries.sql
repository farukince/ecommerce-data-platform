-- Daily revenue
SELECT
    d.date_day,
    COUNT(DISTINCT f.order_key) AS order_count,
    SUM(f.total_amount) AS total_revenue,
    AVG(f.total_amount) AS average_order_value
FROM warehouse.fact_orders f
JOIN warehouse.dim_date d ON f.order_date_key = d.date_key
GROUP BY d.date_day
ORDER BY d.date_day;

-- Category revenue
SELECT
    p.category_name,
    COUNT(DISTINCT fo.order_key) AS order_count,
    SUM(fo.total_amount) AS total_revenue
FROM warehouse.fact_orders fo
JOIN order_items oi ON fo.order_key = oi.order_id
JOIN warehouse.dim_products p ON oi.product_id = p.product_key
GROUP BY p.category_name
ORDER BY total_revenue DESC;

-- Payment status summary
SELECT
    payment_status,
    payment_method,
    COUNT(*) AS payment_count,
    SUM(payment_amount) AS total_payment_amount
FROM warehouse.fact_payments
GROUP BY payment_status, payment_method
ORDER BY payment_count DESC;

-- Shipment performance
SELECT
    cargo_company,
    shipment_status,
    COUNT(*) AS shipment_count,
    AVG(delivery_days) AS avg_delivery_days
FROM warehouse.fact_shipments
GROUP BY cargo_company, shipment_status
ORDER BY shipment_count DESC;

-- Clickstream funnel
SELECT
    event_type,
    COUNT(*) AS event_count,
    COUNT(DISTINCT user_key) AS unique_users
FROM warehouse.fact_clickstream
GROUP BY event_type
ORDER BY event_count DESC;