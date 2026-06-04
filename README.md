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