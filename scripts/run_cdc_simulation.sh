#!/usr/bin/env bash
set -e

echo "Running PostgreSQL CDC simulation..."

python -m pipelines.cdc.postgres_cdc_simulator

echo "CDC simulation completed."