# Data Quality

This document explains the data quality layer of the ecommerce data platform.

The purpose of the data quality layer is to validate cleaned Silver data before it is used by Gold analytics datasets, warehouse models and business queries.

---

## Purpose

Data quality checks help detect problems such as:

- Missing critical identifiers
- Duplicate business records
- Invalid numeric values
- Invalid relationships between tables
- Business-level consistency issues
- Invalid or future event timestamps
- Incomplete shipment and return records

The data quality layer provides a safety checkpoint between cleaned data and downstream analytics.

```text
Silver Data
    ↓
Data Quality Checks
    ↓
Quality Report
    ↓
Gold Analytics / Warehouse Models
```

---

## Data Quality Flow

```text
data_lake/silver/
        ↓
pipelines/quality/data_quality_checks.py
        ↓
pipelines/quality/run_quality_checks.py
        ↓
data_lake/quality_reports/quality_report_YYYY_MM_DD_HHMMSS.json
```

---

## Current Checks

| Check Name | Table | Rule | Purpose |
|---|---|---|---|
| `order_id_not_null` | `orders` | `order_id` must not be null | Ensures every order has a primary identifier |
| `duplicate_orders` | `orders` | `order_id` must be unique | Prevents duplicate order records |
| `payment_amount_non_negative` | `payments` | `payment_amount >= 0` | Prevents invalid payment amounts |
| `order_total_matches_order_items` | `orders`, `order_items` | `orders.total_amount` should match `SUM(quantity * unit_price)` | Validates business-level order amount consistency |
| `delivered_shipments_have_delivered_at` | `shipments` | delivered shipments must have `delivered_at` | Ensures delivered shipments have completion timestamps |
| `returns_have_valid_orders` | `returns`, `orders` | every return must reference an existing `order_id` | Ensures return records are linked to valid orders |
| `event_timestamp_not_in_future` | `click_events`, `cart_events` | `event_timestamp` must not be in the future | Prevents invalid user behavior events |

---

## Check Details

### `order_id_not_null`

Validates that every order has a non-null `order_id`.

```text
orders.order_id IS NOT NULL
```

Why it matters:

- Orders without IDs cannot be joined with payments, shipments, returns or order items.
- Missing order identifiers break downstream fact tables.

---

### `duplicate_orders`

Validates that `order_id` is unique in the orders table.

```text
COUNT(order_id) = COUNT(DISTINCT order_id)
```

Why it matters:

- Duplicate orders can inflate revenue, order count and customer activity metrics.
- Warehouse fact tables usually expect one row per order.

---

### `payment_amount_non_negative`

Validates that payment amounts are not negative.

```text
payments.payment_amount >= 0
```

Why it matters:

- Negative payment values may corrupt revenue and payment analysis.
- Refunds are represented with `payment_status = 'refunded'`, not negative payment amounts.

---

### `order_total_matches_order_items`

Validates that order totals match the sum of order item line amounts.

```text
orders.total_amount = SUM(order_items.quantity * order_items.unit_price)
```

Why it matters:

- This is a business-level consistency check.
- It validates whether the order header amount agrees with item-level details.
- This check helps detect pricing, discount, tax or data generation inconsistencies.

Current project behavior:

```text
orders.total_amount and order_items line totals are generated independently.
```

Because of this, this check may fail in the current synthetic dataset. This is expected and useful because it demonstrates that the data quality layer can detect business-level consistency issues.

---

### `delivered_shipments_have_delivered_at`

Validates that delivered shipments have a delivery timestamp.

```text
shipment_status = 'delivered' → delivered_at IS NOT NULL
```

Why it matters:

- Delivery duration cannot be calculated without `delivered_at`.
- Shipment performance metrics depend on complete delivery timestamps.

---

### `returns_have_valid_orders`

Validates that every return references an existing order.

```text
returns.order_id IN orders.order_id
```

Why it matters:

- Return records without valid orders cannot be used reliably.
- Return rate calculations require valid order relationships.

---

### `event_timestamp_not_in_future`

Validates that clickstream and cart event timestamps are not in the future.

```text
event_timestamp <= current_timestamp
```

Why it matters:

- Future events distort funnel and activity analysis.
- Event-time ordering is important for clickstream analytics.

---

## Report Output

Quality reports are written to:

```text
data_lake/quality_reports/
```

Example file path:

```text
data_lake/quality_reports/quality_report_YYYY_MM_DD_HHMMSS.json
```

Generated quality reports are ignored by Git.

---

## Example Report

```json
{
  "generated_at": "2026-06-02T22:56:37.382840",
  "total_checks": 8,
  "passed_checks": 7,
  "failed_checks": 1,
  "results": [
    {
      "check_name": "order_id_not_null",
      "table_name": "orders",
      "status": "passed",
      "failed_rows": 0,
      "total_rows": 300,
      "description": "order_id must not be null."
    },
    {
      "check_name": "order_total_matches_order_items",
      "table_name": "orders",
      "status": "failed",
      "failed_rows": 300,
      "total_rows": 300,
      "description": "orders.total_amount should match sum(quantity * unit_price) from order_items."
    }
  ]
}
```

---

## Expected Result for Current Synthetic Data

The current synthetic data generator usually produces:

```text
Total checks: 8
Passed checks: 7
Failed checks: 1
```

The expected failing check is:

```text
order_total_matches_order_items
```

Reason:

```text
orders.total_amount and order_items totals are generated independently.
```

This is acceptable for the current project stage because it proves that the data quality layer can catch business-level inconsistencies.

---

## How to Run

Run the full required flow before data quality checks:

```bash
./scripts/reset_env.sh
source .venv/bin/activate
pip install -r requirements.txt

python -m apps.data_generator.main
python -m pipelines.extract.extract_postgres_to_raw
python -m pipelines.transform.run_lakehouse_transformations
python -m pipelines.quality.run_quality_checks
```

Or run the quality step with the helper script:

```bash
./scripts/run_quality_checks.sh
```

---

## How to Inspect Reports

List generated reports:

```bash
find data_lake/quality_reports -type f
```

Show report content:

```bash
cat data_lake/quality_reports/*.json | head -80
```

---

## Data Quality in the Pipeline

The data quality step is part of the Airflow DAG.

```text
transform_bronze_to_silver
        ↓
run_quality_checks
        ↓
build_gold_tables
```

DAG file:

```text
dags/ecommerce_data_pipeline.py
```

---

## Current Implementation

Main files:

| File | Responsibility |
|---|---|
| `pipelines/quality/data_quality_checks.py` | Contains individual data quality rules |
| `pipelines/quality/run_quality_checks.py` | Runs all checks and writes the JSON report |
| `scripts/run_quality_checks.sh` | Helper script for local execution |
| `data_lake/quality_reports/.gitkeep` | Keeps the reports folder in Git |

---

## Quality Result Fields

Each check result includes:

| Field | Description |
|---|---|
| `check_name` | Name of the data quality rule |
| `table_name` | Main table being checked |
| `status` | `passed` or `failed` |
| `failed_rows` | Number of records that violated the rule |
| `total_rows` | Number of records checked |
| `description` | Human-readable explanation of the rule |

---

## Design Notes

The current implementation is intentionally simple and transparent.

It does not depend on external data quality frameworks. This makes the logic easy to understand and review.

A future version could integrate tools such as:

- Great Expectations
- Soda Core
- dbt tests
- Deequ
- Custom Airflow alerting

---

## Future Improvements

Possible future improvements:

- Add severity levels such as `low`, `medium`, `high`, `critical`
- Add failed row samples to reports
- Add rule-level thresholds
- Add Slack or n8n notifications
- Stop the Airflow DAG when critical checks fail
- Store quality reports in a warehouse table
- Add historical quality trend tracking
- Add Great Expectations or Soda Core validation suites
- Add separate checks for Kafka event data
- Add separate checks for CDC events