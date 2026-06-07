from pathlib import Path

REQUIRED_PATHS = [
    "README.md",
    "docker-compose.yml",
    "database/postgres/001_init_schema.sql",
    "dags/ecommerce_data_pipeline.py",
    "pipelines/extract/extract_postgres_to_raw.py",
    "pipelines/quality/run_quality_checks.py",
    "warehouse/marts/001_create_fact_dimension_tables.sql",
    "scripts/run_local.sh",
]


def test_required_project_files_exist() -> None:
    for path in REQUIRED_PATHS:
        assert Path(path).exists(), f"Missing required project file: {path}"
