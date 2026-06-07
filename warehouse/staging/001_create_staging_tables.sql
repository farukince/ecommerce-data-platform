-- Staging tables placeholder for future ELT workflows.
-- Current warehouse models are built directly from operational PostgreSQL tables.
-- This file is intentionally kept minimal so SQL validation does not fail.

CREATE SCHEMA IF NOT EXISTS staging;

SELECT 1 AS staging_file_ready;