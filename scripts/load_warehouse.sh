#!/usr/bin/env bash
set -e

echo "Creating warehouse fact and dimension models..."

python -m pipelines.load.warehouse_loader

echo "Warehouse models created."