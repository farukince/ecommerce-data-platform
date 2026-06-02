#!/usr/bin/env bash
set -e

echo "Running data quality checks..."

python -m pipelines.quality.run_quality_checks

echo "Data quality checks completed."