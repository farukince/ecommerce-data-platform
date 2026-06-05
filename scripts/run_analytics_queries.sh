#!/usr/bin/env bash
set -e

echo "Running ecommerce analytics queries..."

for query_file in warehouse/analytics/*.sql; do
  echo ""
  echo "Running ${query_file}"
  docker exec -i ecommerce_postgres psql -U ecommerce_user -d ecommerce < "${query_file}"
done

echo ""
echo "Analytics queries completed."