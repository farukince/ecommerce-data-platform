from pipelines.extract.postgres_extractor import extract_table
from pipelines.extract.raw_data_writer import write_json_to_raw_layer


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


def extract_postgres_to_raw() -> None:
    print("Starting PostgreSQL to raw data lake extraction...")

    for table_name in SOURCE_TABLES:
        rows = extract_table(table_name)
        output_path = write_json_to_raw_layer(rows, table_name)

        print(
            f"Extracted table={table_name}, "
            f"rows={len(rows)}, "
            f"output={output_path}"
        )

    print("PostgreSQL to raw data lake extraction completed.")


if __name__ == "__main__":
    extract_postgres_to_raw()