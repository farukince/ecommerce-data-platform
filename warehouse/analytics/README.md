# Ecommerce Analytics Queries

This folder contains analytical SQL queries built on top of the PostgreSQL warehouse layer.

The queries answer Trendyol-like marketplace business questions using fact and dimension tables.

## Query List

### 01_daily_revenue.sql

Answers:

- What is the daily revenue?
- How many orders are created each day?
- What is the average order value?

Main tables:

- `warehouse.fact_orders`
- `warehouse.dim_date`

---

### 02_top_selling_categories.sql

Answers:

- What are the top selling categories?
- Which categories generate the highest revenue?
- Which categories have the highest sold quantity?

Main tables:

- `warehouse.fact_orders`
- `order_items`
- `warehouse.dim_products`

---

### 03_cart_abandonment_rate.sql

Answers:

- What percentage of users add products to cart but do not purchase?

Main tables:

- `warehouse.fact_clickstream`
- `warehouse.fact_orders`

---

### 04_return_rate_by_category.sql

Answers:

- Which categories have the highest return rate?

Main tables:

- `warehouse.fact_returns`
- `order_items`
- `warehouse.dim_products`

---

### 05_payment_failure_rate.sql

Answers:

- What is the payment failure rate by payment method?

Main tables:

- `warehouse.fact_payments`

---

### 06_late_shipment_return_impact.sql

Answers:

- Do late shipments have a higher return rate?

Main tables:

- `warehouse.fact_shipments`
- `warehouse.fact_returns`

## Notes

These queries are designed for portfolio and data engineering practice purposes.  
Some metrics may be affected by the synthetic data generation logic.