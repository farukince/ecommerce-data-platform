# E-Commerce Data Platform

This project is an end-to-end data platform inspired by marketplace-scale e-commerce systems.

It simulates operational and clickstream data, processes data through batch and streaming pipelines, applies data quality checks, and creates analytics-ready warehouse models.

---

## Project Scope

The platform includes:

- Synthetic ecommerce data generation
- PostgreSQL operational database
- Raw / Bronze / Silver / Gold data lake layers
- Data quality checks
- PostgreSQL warehouse fact and dimension models
- Analytical SQL queries
- Kafka event streaming
- CDC simulation
- Spark transformations
- Airflow orchestration
- GitHub Actions CI/CD

---

## Architecture

```text
Python Data Generator
        ↓
PostgreSQL Operational DB
        ↓
CDC / Batch Extract
        ↓
Raw Data Lake - JSON / JSONL
        ↓
Bronze / Silver / Gold Layers
        ↓
Data Quality Checks
        ↓
Warehouse Models - PostgreSQL
        ↓
Analytics Queries
```

Streaming flow:

```text
Python Event Producer
        ↓
Kafka Topics
        ↓
Kafka Consumer
        ↓
data_lake/raw/kafka_events/*.jsonl
```

CDC flow:

```text
PostgreSQL tables
        ↓
updated_at-based change detection
        ↓
CDC event builder
        ↓
data_lake/raw/cdc_events/*.jsonl
```

---

## Documentation

Detailed project documentation is available under the `docs/` folder.

| Document | Description |
|---|---|
| `docs/architecture.md` | High-level architecture and system components |
| `docs/data_model.md` | Operational and warehouse data models |
| `docs/pipeline_design.md` | Batch, streaming, CDC and Airflow pipeline design |
| `docs/data_quality.md` | Data quality checks and report structure |
| `docs/how_to_run.md` | Local setup and execution guide |
| `docs/sample_outputs.md` | Example generated outputs |

---

## Repository Structure

```text
apps/
  data_generator/
  event_producer/

database/
  postgres/
  seeds/

pipelines/
  extract/
  transform/
  quality/
  load/
  cdc/

spark/
  jobs/
  utils/

kafka/
  consumers/
  topics/

warehouse/
  marts/
  analytics/
  staging/

data_lake/
  raw/
  bronze/
  silver/
  gold/
  quality_reports/

dags/
  ecommerce_data_pipeline.py

scripts/
  *.sh

docs/
  *.md

.github/
  workflows/
```

---

## Local Services

The project uses Docker Compose for local services.

Main containers:

| Service | Description |
|---|---|
| `ecommerce_postgres` | PostgreSQL operational and warehouse database |
| `ecommerce_kafka` | Kafka broker |
| `ecommerce_kafka_ui` | Kafka UI |

Start services:

```bash
./scripts/run_local.sh
```

or:

```bash
docker compose up -d
```

Check services:

```bash
docker compose ps
```

Kafka UI:

```text
http://localhost:8085
```

---

## Raw Data Extraction

The raw extraction pipeline reads operational PostgreSQL tables and writes them into the raw data lake layer as JSON files.

Run extraction:

```bash
python -m pipelines.extract.extract_postgres_to_raw
```

or:

```bash
./scripts/extract_raw.sh
```

Example output paths:

```text
data_lake/raw/orders/orders_YYYY_MM_DD_HHMMSS.json
data_lake/raw/payments/payments_YYYY_MM_DD_HHMMSS.json
data_lake/raw/click_events/click_events_YYYY_MM_DD_HHMMSS.json
```

Generated raw files are ignored by Git.

---

## Lakehouse Transformations

The project supports a simple lakehouse-style data flow.

```text
Raw JSON
  ↓
Bronze Parquet
  ↓
Silver Clean Parquet
  ↓
Gold Analytics Data
```

Run Pandas-based transformations:

```bash
python -m pipelines.transform.run_lakehouse_transformations
```

or:

```bash
./scripts/run_lakehouse_transformations.sh
```

Generated outputs:

```text
data_lake/bronze/
data_lake/silver/
data_lake/gold/
```

---

## Spark Lakehouse Transformations

The project includes Spark-based lakehouse transformations for scaling the raw, bronze, silver and gold processing layers.

Spark flow:

```text
Raw JSON
  ↓
Bronze Parquet
  ↓
Silver Clean Parquet
  ↓
Gold Analytics Parquet
```

Run Spark transformations:

```bash
./scripts/run_spark_transformations.sh
```

The Spark runner uses Java 17 for local compatibility.

Spark outputs are written under:

```text
data_lake/bronze/
data_lake/silver/
data_lake/gold/
```

Generated Spark Parquet files are ignored by Git.

---

## Data Quality Checks

The project includes a data quality layer that validates Silver data before analytics usage.

Current checks:

- `order_id_not_null`
- `duplicate_orders`
- `payment_amount_non_negative`
- `order_total_matches_order_items`
- `delivered_shipments_have_delivered_at`
- `returns_have_valid_orders`
- `event_timestamp_not_in_future`

Run quality checks:

```bash
python -m pipelines.quality.run_quality_checks
```

or:

```bash
./scripts/run_quality_checks.sh
```

Quality reports are written to:

```text
data_lake/quality_reports/
```

Generated quality reports are ignored by Git.

---

## Airflow Orchestration

The project includes an Airflow DAG that orchestrates the end-to-end ecommerce data pipeline.

DAG file:

```text
dags/ecommerce_data_pipeline.py
```

Pipeline order:

```text
generate_data
  ↓
extract_postgres_data
  ↓
write_raw_layer
  ↓
transform_raw_to_bronze
  ↓
transform_bronze_to_silver
  ↓
run_quality_checks
  ↓
build_gold_tables
  ↓
load_warehouse
```

Check DAG syntax/imports:

```bash
./scripts/check_airflow_dag_import.sh
```

This script validates the DAG file. It does not run the full pipeline.

---

## Warehouse Models

The project includes a PostgreSQL-based warehouse layer with fact and dimension tables.

Main dimension tables:

- `warehouse.dim_users`
- `warehouse.dim_products`
- `warehouse.dim_categories`
- `warehouse.dim_sellers`
- `warehouse.dim_date`

Main fact tables:

- `warehouse.fact_orders`
- `warehouse.fact_payments`
- `warehouse.fact_shipments`
- `warehouse.fact_returns`
- `warehouse.fact_clickstream`

Run warehouse model creation:

```bash
python -m pipelines.load.warehouse_loader
```

or:

```bash
./scripts/load_warehouse.sh
```

Check warehouse tables:

```bash
docker exec -it ecommerce_postgres psql -U ecommerce_user -d ecommerce
```

Inside `psql`:

```sql
\dt warehouse.*
```

---

## Analytics Queries

The project includes business-oriented SQL queries that answer marketplace analytics questions.

Examples:

- Daily revenue
- Top selling categories
- Cart abandonment rate
- Return rate by category
- Payment failure rate
- Late shipment impact on returns

Query files are located in:

```text
warehouse/analytics/
```

Run all analytics queries:

```bash
./scripts/run_analytics_queries.sh
```

---

## Kafka Event Streaming

The project includes a Kafka-based streaming pipeline for ecommerce events.

Streaming flow:

```text
Python Event Producer
  ↓
Kafka Topics
  ↓
Raw Event Consumer
  ↓
data_lake/raw/kafka_events/*.jsonl
```

Kafka topics:

- `product_viewed`
- `cart_updated`
- `order_created`
- `payment_completed`

Run producer:

```bash
./scripts/run_kafka_producer.sh
```

Run consumer:

```bash
./scripts/run_kafka_consumer.sh
```

Kafka UI:

```text
http://localhost:8085
```

Generated Kafka event files are ignored by Git.

---

## CDC Simulation

The project includes a lightweight CDC simulation based on `updated_at` columns.

CDC flow:

```text
PostgreSQL tables
  ↓
updated_at-based change detection
  ↓
CDC event builder
  ↓
data_lake/raw/cdc_events/*.jsonl
```

Current CDC condition:

```sql
updated_at > last_run_at
AND updated_at <= current_run_at
```

Run CDC simulation:

```bash
./scripts/run_cdc_simulation.sh
```

CDC state is stored in:

```text
data_lake/raw/cdc_state/state.json
```

Generated CDC event and state files are ignored by Git.

> Note: This is an MVP CDC simulation. A future phase can replace this with Debezium + PostgreSQL + Kafka for log-based CDC.

---

## CI/CD

The project uses GitHub Actions for automated validation.

Workflow file:

```text
.github/workflows/ci.yml
```

The CI workflow runs on pull requests to `develop` and pushes to `develop` or `feature/**` branches.

Validation steps:

- Python formatting check with Black
- Python linting with Ruff
- Unit tests with Pytest
- SQL file validation
- Docker Compose configuration validation
- Shell script validation with ShellCheck

Run local validation:

```bash
black --check apps pipelines spark tests dags
ruff check apps pipelines spark tests dags
pytest -q
./scripts/check_sql_files.sh
docker compose config
shellcheck scripts/*.sh
```

---

## Full Local Batch Run

Pandas-based local flow:

```bash
./scripts/reset_env.sh
source .venv/bin/activate
pip install -r requirements.txt

python -m apps.data_generator.main
./scripts/extract_raw.sh
./scripts/run_lakehouse_transformations.sh
./scripts/run_quality_checks.sh
./scripts/load_warehouse.sh
./scripts/run_analytics_queries.sh
```

Spark-based local flow:

```bash
./scripts/reset_env.sh
source .venv/bin/activate
pip install -r requirements.txt

python -m apps.data_generator.main
./scripts/extract_raw.sh
./scripts/run_spark_transformations.sh
./scripts/run_quality_checks.sh
./scripts/load_warehouse.sh
./scripts/run_analytics_queries.sh
```

---

## Generated Data Policy

Generated data files are ignored by Git.

Ignored generated folders:

```text
data_lake/raw/
data_lake/bronze/
data_lake/silver/
data_lake/gold/
data_lake/quality_reports/
```

Only `.gitkeep` files should be committed for empty output folders.

---

## Development Flow

Use feature branches:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
```

After development:

```bash
git add .
git commit -m "feat: describe change"
git push -u origin feature/my-feature
```

Open a pull request:

```text
base: develop
compare: feature/my-feature
```

After merge:

```bash
git checkout develop
git pull origin develop
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```