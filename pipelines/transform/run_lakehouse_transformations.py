from pipelines.transform.bronze_to_silver import convert_all_bronze_to_silver
from pipelines.transform.raw_to_bronze import convert_all_raw_to_bronze
from pipelines.transform.silver_to_gold import build_all_gold_datasets

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


def run_lakehouse_transformations() -> None:
    print("Starting lakehouse transformations...")

    convert_all_raw_to_bronze(SOURCE_TABLES)
    convert_all_bronze_to_silver(SOURCE_TABLES)
    build_all_gold_datasets()

    print("Lakehouse transformations completed.")


if __name__ == "__main__":
    run_lakehouse_transformations()
