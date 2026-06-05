#!/usr/bin/env bash
set -e

echo "Running Kafka raw event consumer..."

python -m kafka.consumers.raw_event_consumer

echo "Kafka consumer completed."