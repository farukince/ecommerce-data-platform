#!/usr/bin/env bash
set -e

docker compose down -v
docker compose up -d
echo "Local environment has been reset."
