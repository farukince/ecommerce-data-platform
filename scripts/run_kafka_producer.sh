#!/usr/bin/env bash
set -e

echo "Running Kafka ecommerce event producer..."

python -m apps.event_producer.producer

echo "Kafka producer completed."