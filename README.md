# E-Commerce Data Platform

This project is an end-to-end data platform inspired by marketplace-scale e-commerce systems.

It simulates operational and clickstream data, processes data through batch and streaming pipelines, applies data quality checks, and creates analytics-ready warehouse models.

## Architecture

```text
Python Data Generator
        ↓
PostgreSQL Operational DB
        ↓
CDC / Batch Extract
        ↓
Kafka Event Stream
        ↓
Raw Data Lake - JSON
        ↓
Bronze / Silver / Gold Layers
        ↓
Data Quality Checks
        ↓
Data Warehouse Models (BigQuery/PostgreSQL)
        ↓
Analytics Queries / Dashboard / AI Agent

## Raw Data Extraction

The raw extraction pipeline reads operational PostgreSQL tables and writes them into the raw data lake layer as JSON files.

```bash
python -m pipelines.extract.extract_postgres_to_raw

## Lakehouse Transformations

The project uses a simple lakehouse-style data flow:

```text
Raw JSON
  ↓
Bronze Parquet
  ↓
Silver Clean Parquet
  ↓
Gold Analytics JSON

## Data Quality Checks

The project includes a data quality layer that validates silver data before analytics usage.

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

## Airflow Orchestration

The project includes an Airflow DAG that orchestrates the end-to-end ecommerce data pipeline.

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

<<<<<<< Updated upstream
> Note: This is an MVP CDC simulation. A future phase can replace this with Debezium + PostgreSQL + Kafka for log-based CDC.
=======
> Note: This is an MVP CDC simulation. A future phase can replace this with Debezium + PostgreSQL + Kafka for log-based CDC.

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
>>>>>>> Stashed changes
