# How to Run

This document explains how to run the ecommerce data platform locally.

The project includes:

- PostgreSQL operational database
- Synthetic ecommerce data generator
- Raw data extraction
- Pandas lakehouse transformations
- Spark lakehouse transformations
- Data quality checks
- Warehouse fact and dimension models
- Analytical SQL queries
- Kafka event streaming
- CDC simulation
- Airflow DAG definition
- GitHub Actions validation

---

## Requirements

Recommended local setup:

| Tool | Purpose |
|---|---|
| Python 3.11 or 3.12 | Run Python pipelines and tests |
| Docker Desktop | Run PostgreSQL, Kafka and Kafka UI |
| Git | Version control |
| Java 17 | Run Spark transformations locally |
| VS Code | Development environment |
| ShellCheck | Validate shell scripts locally |

Check Python:

```bash
python --version
```

Check Docker:

```bash
docker --version
docker compose version
```

Check Java:

```bash
java -version
```

Spark transformations require Java 17. The helper script `scripts/run_spark_transformations.sh` tries to use Homebrew Java 17 automatically on macOS.

---

## 1. Clone the Repository

```bash
git clone https://github.com/farukince/ecommerce-data-platform.git
cd ecommerce-data-platform
```

---

## 2. Create and Activate Virtual Environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Environment Variables

Create a local `.env` file from the example file:

```bash
cp .env.example .env
```

Expected local PostgreSQL configuration:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_pass
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

The `.env` file is ignored by Git.

---

## 4. Start Local Services

Start PostgreSQL, Kafka and Kafka UI:

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

Expected containers:

```text
ecommerce_postgres
ecommerce_kafka
ecommerce_kafka_ui
```

Kafka UI:

```text
http://localhost:8085
```

---

## 5. Reset Local Environment

This removes Docker containers and volumes, then starts services from scratch.

```bash
./scripts/reset_env.sh
```

Use this when you want a clean PostgreSQL database.

> Warning: this deletes local PostgreSQL and Kafka Docker volumes.

---

## 6. Generate Synthetic Ecommerce Data

Run:

```bash
python -m apps.data_generator.main
```

This inserts synthetic ecommerce records into PostgreSQL.

Generated entities:

| Entity | Target Table |
|---|---|
| Users | `users` |
| Sellers | `sellers` |
| Categories | `categories` |
| Products | `products` |
| Product inventory | `product_inventory` |
| Orders | `orders` |
| Order items | `order_items` |
| Payments | `payments` |
| Shipments | `shipments` |
| Returns | `returns` |
| Click events | `click_events` |
| Cart events | `cart_events` |

Expected output example:

```text
Starting synthetic ecommerce data generation...
Inserted categories: 8
Inserted sellers: 30
Inserted users: 100
Inserted products: 200
Inserted product_inventory: 200
Inserted orders: 300
Inserted order_items: 700
Inserted payments: 300
Inserted shipments: 250
Inserted returns: 50
Inserted click_events: 1000
Inserted cart_events: 500
Synthetic ecommerce data generation completed.
```

---

## 7. Extract PostgreSQL Tables to Raw Data Lake

Run:

```bash
./scripts/extract_raw.sh
```

or:

```bash
python -m pipelines.extract.extract_postgres_to_raw
```

Output path pattern:

```text
data_lake/raw/<table_name>/<table_name>_YYYY_MM_DD_HHMMSS.json
```

Example outputs:

```text
data_lake/raw/orders/orders_YYYY_MM_DD_HHMMSS.json
data_lake/raw/payments/payments_YYYY_MM_DD_HHMMSS.json
data_lake/raw/click_events/click_events_YYYY_MM_DD_HHMMSS.json
```

Generated raw files are ignored by Git.

---

## 8. Run Pandas Lakehouse Transformations

Run:

```bash
./scripts/run_lakehouse_transformations.sh
```

or:

```bash
python -m pipelines.transform.run_lakehouse_transformations
```

Flow:

```text
Raw JSON
  ↓
Bronze Parquet
  ↓
Silver Clean Parquet
  ↓
Gold Analytics JSON
```

Generated outputs:

```text
data_lake/bronze/
data_lake/silver/
data_lake/gold/
```

---

## 9. Run Spark Lakehouse Transformations

Spark transformations provide a scalable alternative to Pandas transformations.

Run:

```bash
./scripts/run_spark_transformations.sh
```

Flow:

```text
Raw JSON
  ↓
Bronze Parquet
  ↓
Silver Clean Parquet
  ↓
Gold Analytics Parquet
```

The script uses Java 17 for local Spark compatibility.

Expected output examples:

```text
Spark bronze created | table=orders | output=data_lake/bronze/orders
Spark silver created | table=orders | output=data_lake/silver/orders
Spark gold created | dataset=gold_daily_sales_spark | output=data_lake/gold/gold_daily_sales_spark
```

Generated Spark Parquet files are ignored by Git.

---

## 10. Run Data Quality Checks

Before running quality checks, make sure Silver data exists.

Run:

```bash
./scripts/run_quality_checks.sh
```

or:

```bash
python -m pipelines.quality.run_quality_checks
```

Reports are written to:

```text
data_lake/quality_reports/
```

Example summary:

```json
{
  "total_checks": 8,
  "passed_checks": 7,
  "failed_checks": 1
}
```

The expected failing check in the current synthetic dataset may be:

```text
order_total_matches_order_items
```

Reason:

```text
orders.total_amount and order_items totals are generated independently.
```

Generated quality reports are ignored by Git.

---

## 11. Load Warehouse Models

Run:

```bash
./scripts/load_warehouse.sh
```

or:

```bash
python -m pipelines.load.warehouse_loader
```

This creates PostgreSQL warehouse tables under the `warehouse` schema.

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
warehouse.fact_orders
warehouse.fact_payments
warehouse.fact_clickstream
```

Exit `psql`:

```sql
\q
```

---

## 12. Run Analytics Queries

Run:

```bash
./scripts/run_analytics_queries.sh
```

This executes SQL files under:

```text
warehouse/analytics/
```

The analytics queries answer questions such as:

| Business Question | Query File |
|---|---|
| Daily revenue | `01_daily_revenue.sql` |
| Top selling categories | `02_top_selling_categories.sql` |
| Cart abandonment rate | `03_cart_abandonment_rate.sql` |
| Return rate by category | `04_return_rate_by_category.sql` |
| Payment failure rate | `05_payment_failure_rate.sql` |
| Late shipment return impact | `06_late_shipment_return_impact.sql` |

---

## 13. Run Kafka Event Streaming

Start services:

```bash
docker compose up -d
```

Run event producer:

```bash
./scripts/run_kafka_producer.sh
```

Run event consumer:

```bash
./scripts/run_kafka_consumer.sh
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

Kafka topics:

- `product_viewed`
- `cart_updated`
- `order_created`
- `payment_completed`

Kafka UI:

```text
http://localhost:8085
```

Generated Kafka event files are ignored by Git.

---

## 14. Run CDC Simulation

Run:

```bash
./scripts/run_cdc_simulation.sh
```

CDC flow:

```text
PostgreSQL updated_at columns
  ↓
CDC simulator
  ↓
data_lake/raw/cdc_events/*.jsonl
```

First run captures rows changed since the default state timestamp.

Subsequent runs only capture records changed after the previous CDC run.

To test CDC manually:

```bash
docker exec -it ecommerce_postgres psql -U ecommerce_user -d ecommerce
```

Inside `psql`:

```sql
UPDATE orders
SET order_status = 'delivered',
    updated_at = CURRENT_TIMESTAMP
WHERE order_id = 1;

\q
```

Run CDC again:

```bash
./scripts/run_cdc_simulation.sh
```

Expected result:

```text
CDC scanned table=orders, changed_rows=1
```

Generated CDC event and state files are ignored by Git.

---

## 15. Airflow DAG Check

The Airflow DAG is located at:

```text
dags/ecommerce_data_pipeline.py
```

Check DAG syntax/imports:

```bash
./scripts/check_airflow_dag_import.sh
```

This script does not run the full pipeline. It only validates that the DAG file is syntactically valid.

The DAG flow:

```text
start
  ↓
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
  ↓
end
```

---

## 16. Full Local Batch Flow

For a full clean local batch run:

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

With Spark transformations:

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

## 17. Run Local Validation

Before opening a pull request, run:

```bash
black --check apps pipelines spark tests dags
ruff check apps pipelines spark tests dags
pytest -q
./scripts/check_sql_files.sh
docker compose config
shellcheck scripts/*.sh
```

Expected result:

```text
Black: passed
Ruff: passed
Pytest: passed
SQL file check: passed
Docker Compose config: passed
ShellCheck: passed
```

---

## 18. Common Issues

### Docker containers do not appear in Docker Desktop

Check services:

```bash
docker compose ps
```

If no containers are running:

```bash
docker compose up -d
```

---

### PostgreSQL connection fails

Check whether PostgreSQL is healthy:

```bash
docker compose ps
docker compose logs postgres --tail=100
```

---

### Kafka image or startup issue

Check Kafka logs:

```bash
docker compose logs kafka --tail=100
```

Kafka uses:

```text
confluentinc/cp-kafka:7.6.1
```

---

### Spark fails with `getSubject is not supported`

Use Java 17.

Check Java:

```bash
java -version
```

Run Spark through the helper script:

```bash
./scripts/run_spark_transformations.sh
```

The script sets Java 17 automatically when installed through Homebrew.

---

### Generated data appears in Git status

Generated files under the following folders should be ignored:

```text
data_lake/raw/
data_lake/bronze/
data_lake/silver/
data_lake/gold/
data_lake/quality_reports/
```

Check Git status:

```bash
git status
```

If generated data appears, verify `.gitignore`.

---

## 19. Recommended Development Flow

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