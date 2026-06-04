#!/usr/bin/env bash
set -e

echo "Checking Airflow DAG import..."

python -m py_compile dags/ecommerce_data_pipeline.py

echo "DAG file syntax is valid."