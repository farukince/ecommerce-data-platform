-- Impact of late shipments on return rate
-- Assumption: delivery_days > 5 is considered late shipment

WITH shipment_groups AS (
    SELECT
        fs.order_key,
        CASE
            WHEN fs.delivery_days > 5 THEN 'late_shipment'
            WHEN fs.delivery_days IS NULL THEN 'unknown'
            ELSE 'on_time_shipment'
        END AS shipment_group
    FROM warehouse.fact_shipments fs
),

returns AS (
    SELECT DISTINCT
        order_key
    FROM warehouse.fact_returns
)

SELECT
    sg.shipment_group,
    COUNT(DISTINCT sg.order_key) AS shipped_orders,
    COUNT(DISTINCT r.order_key) AS returned_orders,
    ROUND(
        COUNT(DISTINCT r.order_key)::NUMERIC
        / NULLIF(COUNT(DISTINCT sg.order_key), 0),
        4
    ) AS return_rate
FROM shipment_groups sg
LEFT JOIN returns r
    ON sg.order_key = r.order_key
GROUP BY sg.shipment_group
ORDER BY return_rate DESC;