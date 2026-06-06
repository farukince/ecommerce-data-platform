from pathlib import Path

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, to_timestamp

from spark.jobs.raw_to_bronze_spark import SOURCE_TABLES
from spark.utils.spark_session import get_spark_session

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


def read_bronze_table(table_name: str) -> DataFrame:
    spark = get_spark_session("bronze-to-silver-spark")
    input_path = BRONZE_BASE_PATH / table_name

    if not input_path.exists():
        raise FileNotFoundError(f"Bronze path not found: {input_path}")

    return spark.read.parquet(str(input_path))


def apply_common_cleaning(df: DataFrame) -> DataFrame:
    cleaned = df

    for column_name in TIMESTAMP_COLUMNS:
        if column_name in cleaned.columns:
            cleaned = cleaned.withColumn(column_name, to_timestamp(col(column_name)))

    cleaned = cleaned.withColumn("silver_loaded_at", current_timestamp())

    return cleaned


def clean_table(table_name: str, df: DataFrame) -> DataFrame:
    cleaned = apply_common_cleaning(df)

    primary_key = PRIMARY_KEYS.get(table_name)
    if primary_key and primary_key in cleaned.columns:
        cleaned = cleaned.dropDuplicates([primary_key])

    if table_name == "users":
        cleaned = cleaned.dropna(subset=["user_id", "email"])

    if table_name == "products":
        cleaned = cleaned.dropna(subset=["product_id", "category_id", "seller_id"])
        cleaned = cleaned.filter(col("price") >= 0)

    if table_name == "orders":
        cleaned = cleaned.dropna(subset=["order_id", "user_id"])
        cleaned = cleaned.filter(col("total_amount") >= 0)

    if table_name == "order_items":
        cleaned = cleaned.dropna(subset=["order_item_id", "order_id", "product_id"])
        cleaned = cleaned.filter(col("quantity") > 0)
        cleaned = cleaned.filter(col("unit_price") >= 0)

    if table_name == "payments":
        cleaned = cleaned.dropna(subset=["payment_id", "order_id"])
        cleaned = cleaned.filter(col("payment_amount") >= 0)

    if table_name in ["click_events", "cart_events"]:
        cleaned = cleaned.dropna(subset=["event_id", "event_type", "event_timestamp"])

    return cleaned


def convert_bronze_table_to_silver(table_name: str) -> None:
    bronze_df = read_bronze_table(table_name)
    silver_df = clean_table(table_name, bronze_df)

    output_path = SILVER_BASE_PATH / table_name
    silver_df.write.mode("overwrite").parquet(str(output_path))

    print(f"Spark silver created | table={table_name} | output={output_path}")


def convert_all_bronze_to_silver() -> None:
    print("Starting Spark bronze to silver transformation...")

    for table_name in SOURCE_TABLES:
        convert_bronze_table_to_silver(table_name)

    print("Spark bronze to silver transformation completed.")


if __name__ == "__main__":
    convert_all_bronze_to_silver()
