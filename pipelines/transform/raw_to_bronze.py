from pathlib import Path

import pandas as pd


RAW_BASE_PATH = Path("data_lake/raw")
BRONZE_BASE_PATH = Path("data_lake/bronze")


def get_latest_json_file(table_name: str) -> Path:
    table_path = RAW_BASE_PATH / table_name
    json_files = sorted(table_path.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(f"No raw JSON files found for table: {table_name}")

    return json_files[-1]


def convert_raw_table_to_bronze(table_name: str) -> Path:
    input_path = get_latest_json_file(table_name)

    output_dir = BRONZE_BASE_PATH / table_name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{table_name}.parquet"

    df = pd.read_json(input_path)
    df["bronze_loaded_at"] = pd.Timestamp.now()

    df.to_parquet(output_path, index=False)

    print(
        f"Bronze created | table={table_name} | rows={len(df)} | output={output_path}"
    )

    return output_path


def convert_all_raw_to_bronze(table_names: list[str]) -> None:
    print("Starting raw to bronze transformation...")

    for table_name in table_names:
        convert_raw_table_to_bronze(table_name)

    print("Raw to bronze transformation completed.")