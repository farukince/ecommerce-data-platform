-- Daily revenue, order count and average order value

SELECT
    d.date_day,
    COUNT(DISTINCT fo.order_key) AS order_count,
    SUM(fo.total_amount) AS total_revenue,
    ROUND(AVG(fo.total_amount), 2) AS average_order_value
FROM warehouse.fact_orders fo
JOIN warehouse.dim_date d
    ON fo.order_date_key = d.date_key
GROUP BY d.date_day
ORDER BY d.date_day;