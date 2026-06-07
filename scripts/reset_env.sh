#!/usr/bin/env bash
set -e

echo "Stopping and removing local services with volumes..."

docker compose down -v

echo ""
echo "Starting local services from scratch..."

docker compose up -d

echo ""
echo "Local environment has been reset:"
docker compose ps