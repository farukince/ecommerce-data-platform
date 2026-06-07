import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any


def json_serializer(value: Any) -> str | float:
    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    return str(value)


def write_json_to_raw_layer(
    rows: list[dict],
    table_name: str,
    base_path: str = "data_lake/raw",
) -> Path:
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")

    output_dir = Path(base_path) / table_name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{table_name}_{timestamp}.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(
            rows,
            file,
            ensure_ascii=False,
            indent=2,
            default=json_serializer,
        )

    return output_path
