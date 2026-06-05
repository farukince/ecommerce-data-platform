-- Top selling categories by revenue and quantity

SELECT
    dp.category_name,
    COUNT(DISTINCT fo.order_key) AS order_count,
    SUM(fo.total_quantity) AS total_quantity,
    SUM(fo.calculated_items_amount) AS calculated_revenue,
    SUM(fo.total_amount) AS order_revenue
FROM warehouse.fact_orders fo
JOIN order_items oi
    ON fo.order_key = oi.order_id
JOIN warehouse.dim_products dp
    ON oi.product_id = dp.product_key
GROUP BY dp.category_name
ORDER BY calculated_revenue DESC;