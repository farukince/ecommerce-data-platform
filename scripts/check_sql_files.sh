#!/usr/bin/env bash
set -e

echo "Checking SQL files..."

SQL_FILES=$(find database warehouse -name "*.sql" -type f)

if [ -z "$SQL_FILES" ]; then
  echo "No SQL files found."
  exit 1
fi

for file in $SQL_FILES; do
  echo "Checking $file"

  if [ ! -s "$file" ]; then
    echo "SQL file is empty: $file"
    exit 1
  fi

  if grep -q $'\r' "$file"; then
    echo "SQL file contains Windows CRLF characters: $file"
    exit 1
  fi
done

echo "SQL files check completed."