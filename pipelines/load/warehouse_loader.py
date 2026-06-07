from pathlib import Path

from apps.data_generator.db import get_engine

WAREHOUSE_SQL_PATH = Path("warehouse/marts/001_create_fact_dimension_tables.sql")


def load_warehouse_models() -> None:
    if not WAREHOUSE_SQL_PATH.exists():
        raise FileNotFoundError(f"Warehouse SQL file not found: {WAREHOUSE_SQL_PATH}")

    sql = WAREHOUSE_SQL_PATH.read_text(encoding="utf-8")
    engine = get_engine()

    print("Starting warehouse model creation...")

    with engine.begin() as connection:
        connection.exec_driver_sql(sql)

    print("Warehouse fact and dimension models created successfully.")


if __name__ == "__main__":
    load_warehouse_models()
