#!/usr/bin/env bash
set -e

echo "Running PostgreSQL to raw data lake extraction..."

python -m pipelines.extract.extract_postgres_to_raw

echo "Raw data extraction completed."