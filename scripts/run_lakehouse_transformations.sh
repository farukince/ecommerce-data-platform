#!/usr/bin/env bash
set -e

echo "Running lakehouse transformations..."

python -m pipelines.transform.run_lakehouse_transformations

echo "Lakehouse transformations completed."