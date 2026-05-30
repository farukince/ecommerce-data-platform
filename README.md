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