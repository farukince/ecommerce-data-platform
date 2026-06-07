#!/usr/bin/env bash
set -e

echo "Checking Airflow DAG syntax..."

python -m py_compile dags/ecommerce_data_pipeline.py

echo "DAG syntax is valid."

echo "Checking optional Airflow import..."

python - << 'EOF'
try:
    from airflow.operators.empty import EmptyOperator
    from airflow.operators.python import PythonOperator
    print("Airflow imports are valid.")
except ImportError:
    print("Airflow is not installed or import path is unavailable in this environment.")
EOF