from pathlib import Path

from pyspark.sql.functions import current_timestamp

from spark.utils.spark_session import get_spark_session


RAW_BASE_PATH = Path("data_lake/raw")
BRONZE_BASE_PATH = Path("data_lake/bronze")


SOURCE_TABLES = [
    "users",
    "sellers",
    "categories",
    "products",
    "product_inventory",
    "orders",
    "order_items",
    "payments",
    "shipments",
    "returns",
    "click_events",
    "cart_events",
]


def get_latest_json_file(table_name: str) -> str:
    table_path = RAW_BASE_PATH / table_name
    json_files = sorted(table_path.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(f"No raw JSON files found for table: {table_name}")

    return str(json_files[-1])


def convert_raw_table_to_bronze(table_name: str) -> None:
    spark = get_spark_session("raw-to-bronze-spark")

    input_path = get_latest_json_file(table_name)
    output_path = BRONZE_BASE_PATH / table_name

    df = spark.read.option("multiline", "true").json(input_path)
    df = df.withColumn("bronze_loaded_at", current_timestamp())

    df.write.mode("overwrite").parquet(str(output_path))

    print(f"Spark bronze created | table={table_name} | output={output_path}")


def convert_all_raw_to_bronze() -> None:
    print("Starting Spark raw to bronze transformation...")

    for table_name in SOURCE_TABLES:
        convert_raw_table_to_bronze(table_name)

    print("Spark raw to bronze transformation completed.")


if __name__ == "__main__":
    convert_all_raw_to_bronze()