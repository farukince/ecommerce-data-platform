from sqlalchemy import text

from apps.data_generator.db import get_engine


def extract_table(table_name: str) -> list[dict]:
    engine = get_engine()

    query = text(f"SELECT * FROM {table_name}")

    with engine.connect() as connection:
        result = connection.execute(query)
        rows = result.mappings().all()

    return [dict(row) for row in rows]