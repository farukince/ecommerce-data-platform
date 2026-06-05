DROP SCHEMA IF EXISTS warehouse CASCADE;
CREATE SCHEMA warehouse;

CREATE TABLE warehouse.dim_users AS
SELECT
    user_id AS user_key,
    full_name,
    email,
    city,
    created_at,
    updated_at
FROM users;

ALTER TABLE warehouse.dim_users ADD PRIMARY KEY (user_key);

CREATE TABLE warehouse.dim_categories AS
SELECT
    category_id AS category_key,
    category_name,
    created_at,
    updated_at
FROM categories;

ALTER TABLE warehouse.dim_categories ADD PRIMARY KEY (category_key);

CREATE TABLE warehouse.dim_sellers AS
SELECT
    seller_id AS seller_key,
    seller_name,
    seller_city,
    seller_score,
    is_active,
    created_at,
    updated_at
FROM sellers;

ALTER TABLE warehouse.dim_sellers ADD PRIMARY KEY (seller_key);

CREATE TABLE warehouse.dim_products AS
SELECT
    p.product_id AS product_key,
    p.product_name,
    p.brand,
    p.price,
    p.product_status,
    p.category_id AS category_key,
    c.category_name,
    p.seller_id AS seller_key,
    s.seller_name,
    p.created_at,
    p.updated_at
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN sellers s ON p.seller_id = s.seller_id;

ALTER TABLE warehouse.dim_products ADD PRIMARY KEY (product_key);

CREATE TABLE warehouse.dim_date AS
WITH date_range AS (
    SELECT generate_series(
        COALESCE((SELECT MIN(order_date)::date FROM orders), CURRENT_DATE - INTERVAL '30 days'),
        COALESCE((SELECT MAX(order_date)::date FROM orders), CURRENT_DATE),
        INTERVAL '1 day'
    )::date AS date_day
)
SELECT
    TO_CHAR(date_day, 'YYYYMMDD')::INT AS date_key,
    date_day,
    EXTRACT(YEAR FROM date_day)::INT AS year,
    EXTRACT(MONTH FROM date_day)::INT AS month,
    EXTRACT(DAY FROM date_day)::INT AS day,
    EXTRACT(QUARTER FROM date_day)::INT AS quarter,
    EXTRACT(ISODOW FROM date_day)::INT AS iso_day_of_week,
    TO_CHAR(date_day, 'Day') AS day_name,
    TO_CHAR(date_day, 'Month') AS month_name
FROM date_range;

ALTER TABLE warehouse.dim_date ADD PRIMARY KEY (date_key);

CREATE TABLE warehouse.fact_orders AS
SELECT
    o.order_id AS order_key,
    o.user_id AS user_key,
    TO_CHAR(o.order_date::date, 'YYYYMMDD')::INT AS order_date_key,
    o.order_status,
    o.total_amount,
    COUNT(oi.order_item_id) AS item_count,
    COALESCE(SUM(oi.quantity), 0) AS total_quantity,
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS calculated_items_amount,
    o.created_at,
    o.updated_at
FROM orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY
    o.order_id,
    o.user_id,
    o.order_date,
    o.order_status,
    o.total_amount,
    o.created_at,
    o.updated_at;

ALTER TABLE warehouse.fact_orders ADD PRIMARY KEY (order_key);

CREATE TABLE warehouse.fact_payments AS
SELECT
    p.payment_id AS payment_key,
    p.order_id AS order_key,
    o.user_id AS user_key,
    TO_CHAR(COALESCE(p.paid_at, p.created_at)::date, 'YYYYMMDD')::INT AS payment_date_key,
    p.payment_status,
    p.payment_method,
    p.payment_amount,
    p.paid_at,
    p.created_at,
    p.updated_at
FROM payments p
LEFT JOIN orders o ON p.order_id = o.order_id;

ALTER TABLE warehouse.fact_payments ADD PRIMARY KEY (payment_key);

CREATE TABLE warehouse.fact_shipments AS
SELECT
    s.shipment_id AS shipment_key,
    s.order_id AS order_key,
    o.user_id AS user_key,
    TO_CHAR(COALESCE(s.shipped_at, s.created_at)::date, 'YYYYMMDD')::INT AS shipment_date_key,
    s.shipment_status,
    s.cargo_company,
    s.tracking_number,
    s.shipped_at,
    s.delivered_at,
    CASE
        WHEN s.shipped_at IS NOT NULL AND s.delivered_at IS NOT NULL
        THEN EXTRACT(DAY FROM (s.delivered_at - s.shipped_at))::INT
        ELSE NULL
    END AS delivery_days,
    s.created_at,
    s.updated_at
FROM shipments s
LEFT JOIN orders o ON s.order_id = o.order_id;

ALTER TABLE warehouse.fact_shipments ADD PRIMARY KEY (shipment_key);

CREATE TABLE warehouse.fact_returns AS
SELECT
    r.return_id AS return_key,
    r.order_id AS order_key,
    o.user_id AS user_key,
    TO_CHAR(COALESCE(r.returned_at, r.created_at)::date, 'YYYYMMDD')::INT AS return_date_key,
    r.return_reason,
    r.return_status,
    r.returned_at,
    r.created_at,
    r.updated_at
FROM returns r
LEFT JOIN orders o ON r.order_id = o.order_id;

ALTER TABLE warehouse.fact_returns ADD PRIMARY KEY (return_key);

CREATE TABLE warehouse.fact_clickstream AS
SELECT
    CONCAT('click_', event_id)::TEXT AS event_key,
    event_id AS source_event_id,
    'click_event' AS event_source,
    user_id AS user_key,
    product_id AS product_key,
    TO_CHAR(event_timestamp::date, 'YYYYMMDD')::INT AS event_date_key,
    event_type,
    page_url,
    device_type,
    session_id,
    NULL::INT AS quantity,
    NULL::TEXT AS cart_id,
    event_timestamp
FROM click_events

UNION ALL

SELECT
    CONCAT('cart_', event_id)::TEXT AS event_key,
    event_id AS source_event_id,
    'cart_event' AS event_source,
    user_id AS user_key,
    product_id AS product_key,
    TO_CHAR(event_timestamp::date, 'YYYYMMDD')::INT AS event_date_key,
    event_type,
    NULL::TEXT AS page_url,
    NULL::TEXT AS device_type,
    session_id,
    quantity,
    cart_id,
    event_timestamp
FROM cart_events;

ALTER TABLE warehouse.fact_clickstream ADD PRIMARY KEY (event_key);

CREATE INDEX idx_fact_orders_user_key ON warehouse.fact_orders(user_key);
CREATE INDEX idx_fact_orders_order_date_key ON warehouse.fact_orders(order_date_key);
CREATE INDEX idx_fact_payments_order_key ON warehouse.fact_payments(order_key);
CREATE INDEX idx_fact_shipments_order_key ON warehouse.fact_shipments(order_key);
CREATE INDEX idx_fact_returns_order_key ON warehouse.fact_returns(order_key);
CREATE INDEX idx_fact_clickstream_user_key ON warehouse.fact_clickstream(user_key);
CREATE INDEX idx_fact_clickstream_product_key ON warehouse.fact_clickstream(product_key);
CREATE INDEX idx_fact_clickstream_event_date_key ON warehouse.fact_clickstream(event_date_key);