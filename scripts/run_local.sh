#!/usr/bin/env bash
set -e

echo "Starting local services..."

docker compose up -d

echo ""
echo "Local services are running:"
docker compose ps