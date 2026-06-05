-- Return rate by product category

WITH orders_by_category AS (
    SELECT
        dp.category_name,
        COUNT(DISTINCT fo.order_key) AS order_count
    FROM warehouse.fact_orders fo
    JOIN order_items oi
        ON fo.order_key = oi.order_id
    JOIN warehouse.dim_products dp
        ON oi.product_id = dp.product_key
    GROUP BY dp.category_name
),

returns_by_category AS (
    SELECT
        dp.category_name,
        COUNT(DISTINCT fr.return_key) AS return_count
    FROM warehouse.fact_returns fr
    JOIN order_items oi
        ON fr.order_key = oi.order_id
    JOIN warehouse.dim_products dp
        ON oi.product_id = dp.product_key
    GROUP BY dp.category_name
)

SELECT
    obc.category_name,
    obc.order_count,
    COALESCE(rbc.return_count, 0) AS return_count,
    ROUND(
        COALESCE(rbc.return_count, 0)::NUMERIC
        / NULLIF(obc.order_count, 0),
        4
    ) AS return_rate
FROM orders_by_category obc
LEFT JOIN returns_by_category rbc
    ON obc.category_name = rbc.category_name
ORDER BY return_rate DESC, return_count DESC;