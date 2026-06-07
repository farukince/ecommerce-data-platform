# Sample Outputs

This document describes the main generated outputs of the ecommerce data platform.

Generated data files are ignored by Git and should not be committed.

The goal of this document is to show:

- Where output files are created
- What file formats are used
- What sample records look like
- How to inspect outputs locally

---

## Output Overview

| Pipeline Step | Output Location | Format |
|---|---|---|
| Raw PostgreSQL extraction | `data_lake/raw/<table_name>/` | JSON |
| Kafka event consumer | `data_lake/raw/kafka_events/` | JSONL |
| CDC simulation | `data_lake/raw/cdc_events/` | JSONL |
| Bronze layer | `data_lake/bronze/<table_name>/` | Parquet |
| Silver layer | `data_lake/silver/<table_name>/` | Parquet |
| Gold layer | `data_lake/gold/<dataset_name>/` | JSON or Parquet |
| Data quality reports | `data_lake/quality_reports/` | JSON |
| Warehouse models | PostgreSQL `warehouse` schema | SQL tables |
| Analytics queries | Terminal output | SQL result sets |

---

## Raw Data Lake Outputs

Raw PostgreSQL extracts are written as JSON files.

Example path pattern:

```text
data_lake/raw/<table_name>/<table_name>_YYYY_MM_DD_HHMMSS.json
```

Example paths:

```text
data_lake/raw/users/users_YYYY_MM_DD_HHMMSS.json
data_lake/raw/orders/orders_YYYY_MM_DD_HHMMSS.json
data_lake/raw/payments/payments_YYYY_MM_DD_HHMMSS.json
data_lake/raw/click_events/click_events_YYYY_MM_DD_HHMMSS.json
data_lake/raw/cart_events/cart_events_YYYY_MM_DD_HHMMSS.json
```

Example raw order record:

```json
{
  "order_id": 1,
  "user_id": 42,
  "order_status": "paid",
  "order_date": "2026-06-05T04:21:30",
  "total_amount": 1250.75,
  "created_at": "2026-06-05T04:21:30",
  "updated_at": "2026-06-05T04:21:30"
}
```

Inspect raw files:

```bash
find data_lake/raw -type f | head
head -40 data_lake/raw/orders/*.json
```

---

## Kafka Raw Event Outputs

Kafka consumer writes streamed events as JSONL files.

JSONL means each line is a separate JSON event.

Example path pattern:

```text
data_lake/raw/kafka_events/kafka_events_YYYY_MM_DD_HHMMSS.jsonl
```

Example Kafka event:

```json
{
  "event_id": "8c37d6b9-2a4d-4b14-96d2-8b5f4a5d10a1",
  "event_type": "product_viewed",
  "event_timestamp": "2026-06-05T04:30:00",
  "user_id": 42,
  "session_id": "c4c4e4d7-3e28-4f5d-bdf4-7217a9e75a33",
  "source": "kafka_stream",
  "product_id": 17,
  "device_type": "mobile",
  "page_url": "/products/17",
  "_kafka_topic": "product_viewed",
  "_kafka_partition": 0,
  "_kafka_offset": 12,
  "_consumed_at": "2026-06-05T04:31:00"
}
```

Inspect Kafka event files:

```bash
find data_lake/raw/kafka_events -type f
head -5 data_lake/raw/kafka_events/*.jsonl
```

---

## CDC Event Outputs

CDC simulation writes changed PostgreSQL records as JSONL files.

Example path pattern:

```text
data_lake/raw/cdc_events/cdc_events_YYYY_MM_DD_HHMMSS.jsonl
```

Example CDC event:

```json
{
  "operation": "upsert",
  "source": "postgres_cdc_simulation",
  "table_name": "orders",
  "changed_at": "2026-06-05T04:02:28",
  "captured_at": "2026-06-05T04:03:51",
  "data": {
    "order_id": 1,
    "user_id": 42,
    "order_status": "delivered",
    "total_amount": 1250.75,
    "updated_at": "2026-06-05T04:02:28"
  }
}
```

CDC state file:

```text
data_lake/raw/cdc_state/state.json
```

Example state:

```json
{
  "last_run_at": "2026-06-05T04:03:51"
}
```

Inspect CDC outputs:

```bash
find data_lake/raw/cdc_events -type f
tail -5 data_lake/raw/cdc_events/*.jsonl
cat data_lake/raw/cdc_state/state.json
```

---

## Bronze Layer Outputs

Bronze data is written as Parquet.

The Bronze layer converts raw JSON into a more efficient analytical format.

Example paths:

```text
data_lake/bronze/users/
data_lake/bronze/orders/
data_lake/bronze/payments/
data_lake/bronze/click_events/
```

Spark usually writes Parquet as folder-based outputs:

```text
data_lake/bronze/orders/part-00000-....snappy.parquet
```

Inspect Bronze outputs:

```bash
find data_lake/bronze -type f | head
```

---

## Silver Layer Outputs

Silver data is cleaned and standardized.

Cleaning examples:

- Timestamp conversion
- Duplicate removal
- Null filtering for critical identifiers
- Negative value filtering
- Event timestamp validation

Example paths:

```text
data_lake/silver/users/
data_lake/silver/orders/
data_lake/silver/payments/
data_lake/silver/click_events/
```

Spark usually writes:

```text
data_lake/silver/orders/part-00000-....snappy.parquet
```

Inspect Silver outputs:

```bash
find data_lake/silver -type f | head
```

---

## Gold Layer Outputs

Gold datasets are analytics-ready outputs.

Current Gold datasets:

| Dataset | Description |
|---|---|
| `gold_daily_sales` | Daily order count, revenue and average order value |
| `gold_category_sales` | Category-level revenue and quantity metrics |
| `gold_payment_summary` | Payment method and payment status summary |
| `gold_conversion_funnel` | Product view, cart add and purchase funnel |

Example paths:

```text
data_lake/gold/gold_daily_sales/
data_lake/gold/gold_category_sales/
data_lake/gold/gold_payment_summary/
data_lake/gold/gold_conversion_funnel/
```

Spark Gold outputs use Parquet:

```text
data_lake/gold/gold_daily_sales_spark/part-00000-....snappy.parquet
data_lake/gold/gold_category_sales_spark/part-00000-....snappy.parquet
```

Example `gold_daily_sales` record:

```json
{
  "order_day": "2026-06-05",
  "order_count": 34,
  "total_revenue": 82500.25,
  "average_order_value": 2426.48
}
```

Inspect Gold outputs:

```bash
find data_lake/gold -type f | head
```

---

## Data Quality Report Outputs

Data quality reports are written as JSON files.

Example path pattern:

```text
data_lake/quality_reports/quality_report_YYYY_MM_DD_HHMMSS.json
```

Example summary:

```json
{
  "generated_at": "2026-06-02T22:56:37.382840",
  "total_checks": 8,
  "passed_checks": 7,
  "failed_checks": 1
}
```

Example check result:

```json
{
  "check_name": "order_total_matches_order_items",
  "table_name": "orders",
  "status": "failed",
  "failed_rows": 300,
  "total_rows": 300,
  "description": "orders.total_amount should match sum(quantity * unit_price) from order_items."
}
```

Inspect quality reports:

```bash
find data_lake/quality_reports -type f
cat data_lake/quality_reports/*.json | head -80
```

---

## Warehouse Outputs

Warehouse models are created in PostgreSQL under the `warehouse` schema.

Check warehouse tables:

```bash
docker exec -it ecommerce_postgres psql -U ecommerce_user -d ecommerce
```

Inside `psql`:

```sql
\dt warehouse.*
```

Example warehouse tables:

```text
warehouse.dim_users
warehouse.dim_products
warehouse.dim_categories
warehouse.dim_sellers
warehouse.dim_date
warehouse.fact_orders
warehouse.fact_payments
warehouse.fact_shipments
warehouse.fact_returns
warehouse.fact_clickstream
```

Example count checks:

```sql
SELECT COUNT(*) FROM warehouse.dim_users;
SELECT COUNT(*) FROM warehouse.dim_products;
SELECT COUNT(*) FROM warehouse.fact_orders;
SELECT COUNT(*) FROM warehouse.fact_clickstream;
```

Exit:

```sql
\q
```

---

## Analytics Query Outputs

Analytics SQL files are located in:

```text
warehouse/analytics/
```

Run all analytics queries:

```bash
./scripts/run_analytics_queries.sh
```

Example query output: daily revenue.

```text
 date_day   | order_count | total_revenue | average_order_value
------------+-------------+---------------+---------------------
 2026-06-01 |          12 |      24500.50 |             2041.71
 2026-06-02 |          18 |      38620.30 |             2145.57
 2026-06-03 |          15 |      31240.90 |             2082.73
```

Example query output: payment failure rate.

```text
 payment_method | total_payment_attempts | successful_payments | failed_payments | payment_failure_rate
----------------+------------------------+---------------------+-----------------+----------------------
 credit_card    |                     80 |                  58 |              14 |               0.1750
 wallet         |                     65 |                  50 |               8 |               0.1231
```

---

## Airflow DAG Check Output

The Airflow DAG check script validates syntax and imports.

Run:

```bash
./scripts/check_airflow_dag_import.sh
```

Example output:

```text
Checking Airflow DAG syntax...
DAG syntax is valid.
Checking optional Airflow import...
Airflow imports are valid.
```

This script does not generate data files.

---

## Spark Output Example

Run Spark transformations:

```bash
./scripts/run_spark_transformations.sh
```

Example terminal output:

```text
Using Java:
openjdk version "17.0.19"

Running Spark lakehouse transformations...
Starting Spark lakehouse transformations...
Starting Spark raw to bronze transformation...
Spark bronze created | table=orders | output=data_lake/bronze/orders
Spark raw to bronze transformation completed.
Starting Spark bronze to silver transformation...
Spark silver created | table=orders | output=data_lake/silver/orders
Spark bronze to silver transformation completed.
Starting Spark silver to gold transformation...
Spark gold created | dataset=gold_daily_sales_spark | output=data_lake/gold/gold_daily_sales_spark
Spark silver to gold transformation completed.
Spark lakehouse transformations completed.
```

---

## Git Ignore Behavior

Generated data outputs should not appear in Git status.

Ignored generated folders:

```text
data_lake/raw/
data_lake/bronze/
data_lake/silver/
data_lake/gold/
data_lake/quality_reports/
```

Check:

```bash
git status
```

Expected behavior:

```text
No generated JSON, JSONL or Parquet files should be staged for commit.
```

Only `.gitkeep` files should be committed for empty output folders.

---

## Notes

The sample values in this document are examples.

Actual values will change each time because the project uses synthetic data generation with random values.