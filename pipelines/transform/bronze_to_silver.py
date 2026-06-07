from pathlib import Path

import pandas as pd

BRONZE_BASE_PATH = Path("data_lake/bronze")
SILVER_BASE_PATH = Path("data_lake/silver")


PRIMARY_KEYS = {
    "users": "user_id",
    "sellers": "seller_id",
    "categories": "category_id",
    "products": "product_id",
    "product_inventory": "inventory_id",
    "orders": "order_id",
    "order_items": "order_item_id",
    "payments": "payment_id",
    "shipments": "shipment_id",
    "returns": "return_id",
    "click_events": "event_id",
    "cart_events": "event_id",
}


TIMESTAMP_COLUMNS = [
    "created_at",
    "updated_at",
    "order_date",
    "paid_at",
    "shipped_at",
    "delivered_at",
    "returned_at",
    "event_timestamp",
    "bronze_loaded_at",
]


def read_bronze_table(table_name: str) -> pd.DataFrame:
    input_path = BRONZE_BASE_PATH / table_name / f"{table_name}.parquet"

    if not input_path.exists():
        raise FileNotFoundError(f"Bronze file not found: {input_path}")

    return pd.read_parquet(input_path)


def clean_common_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    for column in TIMESTAMP_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")

    cleaned["silver_loaded_at"] = pd.Timestamp.now()

    return cleaned


def clean_table(table_name: str, df: pd.DataFrame) -> pd.DataFrame:
    cleaned = clean_common_columns(df)

    primary_key = PRIMARY_KEYS.get(table_name)
    if primary_key and primary_key in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset=[primary_key])

    if table_name == "users":
        cleaned = cleaned.dropna(subset=["user_id", "email"])

    if table_name == "products":
        cleaned = cleaned.dropna(subset=["product_id", "category_id", "seller_id"])
        cleaned = cleaned[cleaned["price"] >= 0]

    if table_name == "orders":
        cleaned = cleaned.dropna(subset=["order_id", "user_id"])
        cleaned = cleaned[cleaned["total_amount"] >= 0]

    if table_name == "order_items":
        cleaned = cleaned.dropna(subset=["order_item_id", "order_id", "product_id"])
        cleaned = cleaned[cleaned["quantity"] > 0]
        cleaned = cleaned[cleaned["unit_price"] >= 0]

    if table_name == "payments":
        cleaned = cleaned.dropna(subset=["payment_id", "order_id"])
        cleaned = cleaned[cleaned["payment_amount"] >= 0]

    if table_name in ["click_events", "cart_events"]:
        cleaned = cleaned.dropna(subset=["event_id", "event_type", "event_timestamp"])

    return cleaned.reset_index(drop=True)


def write_silver_table(table_name: str, df: pd.DataFrame) -> Path:
    output_dir = SILVER_BASE_PATH / table_name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{table_name}.parquet"
    df.to_parquet(output_path, index=False)

    print(
        f"Silver created | table={table_name} | rows={len(df)} | output={output_path}"
    )

    return output_path


def convert_bronze_table_to_silver(table_name: str) -> Path:
    bronze_df = read_bronze_table(table_name)
    silver_df = clean_table(table_name, bronze_df)

    return write_silver_table(table_name, silver_df)


def convert_all_bronze_to_silver(table_names: list[str]) -> None:
    print("Starting bronze to silver transformation...")

    for table_name in table_names:
        convert_bronze_table_to_silver(table_name)

    print("Bronze to silver transformation completed.")
