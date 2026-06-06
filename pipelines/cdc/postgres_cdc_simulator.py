import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy import text

from apps.data_generator.db import get_engine
from pipelines.cdc.cdc_state import load_state, save_state

CDC_OUTPUT_PATH = Path("data_lake/raw/cdc_events")


CDC_TABLES = {
    "users": "updated_at",
    "sellers": "updated_at",
    "categories": "updated_at",
    "products": "updated_at",
    "product_inventory": "updated_at",
    "orders": "updated_at",
    "payments": "updated_at",
    "shipments": "updated_at",
    "returns": "updated_at",
}


def json_serializer(value: Any) -> str | float:
    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    return str(value)


def normalize_last_run_at(value: str) -> datetime:
    return datetime.fromisoformat(value)


def get_database_current_timestamp() -> datetime:
    engine = get_engine()

    query = text("SELECT CURRENT_TIMESTAMP::timestamp AS current_run_at")

    with engine.connect() as connection:
        result = connection.execute(query).mappings().one()

    return result["current_run_at"]


def fetch_changed_rows(
    table_name: str,
    updated_at_column: str,
    last_run_at: datetime,
    current_run_at: datetime,
) -> list[dict]:
    engine = get_engine()

    query = text(f"""
        SELECT *
        FROM {table_name}
        WHERE {updated_at_column} > :last_run_at
          AND {updated_at_column} <= :current_run_at
        ORDER BY {updated_at_column}
        """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "last_run_at": last_run_at,
                "current_run_at": current_run_at,
            },
        )
        rows = result.mappings().all()

    return [dict(row) for row in rows]


def build_cdc_event(
    table_name: str,
    updated_at_column: str,
    row: dict,
) -> dict:
    return {
        "operation": "upsert",
        "source": "postgres_cdc_simulation",
        "table_name": table_name,
        "changed_at": row.get(updated_at_column),
        "captured_at": datetime.now(),
        "data": row,
    }


def write_cdc_events(events: list[dict]) -> Path | None:
    if not events:
        print("No CDC events to write.")
        return None

    CDC_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    output_path = CDC_OUTPUT_PATH / f"cdc_events_{timestamp}.jsonl"

    with output_path.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(
                json.dumps(
                    event,
                    ensure_ascii=False,
                    default=json_serializer,
                )
                + "\n"
            )

    return output_path


def run_cdc_simulation() -> None:
    print("Starting PostgreSQL CDC simulation...")

    state = load_state()
    last_run_at = normalize_last_run_at(state["last_run_at"])
    current_run_at = get_database_current_timestamp()

    print(f"Last run timestamp: {last_run_at.isoformat()}")
    print(f"Current run timestamp: {current_run_at.isoformat()}")

    all_events = []

    for table_name, updated_at_column in CDC_TABLES.items():
        rows = fetch_changed_rows(
            table_name=table_name,
            updated_at_column=updated_at_column,
            last_run_at=last_run_at,
            current_run_at=current_run_at,
        )

        for row in rows:
            all_events.append(
                build_cdc_event(
                    table_name=table_name,
                    updated_at_column=updated_at_column,
                    row=row,
                )
            )

        print(f"CDC scanned table={table_name}, changed_rows={len(rows)}")

    output_path = write_cdc_events(all_events)

    if output_path:
        print(f"CDC events written to: {output_path}")

    save_state(current_run_at)

    print(f"CDC state updated: last_run_at={current_run_at.isoformat()}")
    print("PostgreSQL CDC simulation completed.")


if __name__ == "__main__":
    run_cdc_simulation()
