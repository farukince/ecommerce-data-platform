from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from apps.data_generator.config import DatabaseConfig


def get_engine() -> Engine:
    config = DatabaseConfig()
    return create_engine(config.sqlalchemy_url, pool_pre_ping=True)


def execute_many(engine: Engine, query: str, rows: list[dict]) -> None:
    if not rows:
        return

    with engine.begin() as connection:
        connection.execute(text(query), rows)


def fetch_ids(engine: Engine, table_name: str, id_column: str) -> list[int]:
    query = text(f"SELECT {id_column} FROM {table_name}")

    with engine.connect() as connection:
        result = connection.execute(query)
        return [row[0] for row in result.fetchall()]