-- Cart abandonment rate
-- Users who added product to cart but did not create an order

WITH cart_users AS (
    SELECT DISTINCT
        user_key
    FROM warehouse.fact_clickstream
    WHERE event_source = 'cart_event'
      AND event_type = 'product_added_to_cart'
      AND user_key IS NOT NULL
),

purchasers AS (
    SELECT DISTINCT
        user_key
    FROM warehouse.fact_orders
    WHERE user_key IS NOT NULL
),

cart_without_purchase AS (
    SELECT
        cu.user_key
    FROM cart_users cu
    LEFT JOIN purchasers p
        ON cu.user_key = p.user_key
    WHERE p.user_key IS NULL
)

SELECT
    COUNT(DISTINCT cu.user_key) AS cart_users,
    COUNT(DISTINCT p.user_key) AS purchasing_users,
    COUNT(DISTINCT cwp.user_key) AS cart_abandoned_users,
    ROUND(
        COUNT(DISTINCT cwp.user_key)::NUMERIC
        / NULLIF(COUNT(DISTINCT cu.user_key), 0),
        4
    ) AS cart_abandonment_rate
FROM cart_users cu
LEFT JOIN purchasers p
    ON cu.user_key = p.user_key
LEFT JOIN cart_without_purchase cwp
    ON cu.user_key = cwp.user_key;