from spark.jobs.bronze_to_silver_spark import convert_all_bronze_to_silver
from spark.jobs.raw_to_bronze_spark import convert_all_raw_to_bronze
from spark.jobs.silver_to_gold_spark import build_all_gold_datasets


def run_spark_lakehouse_transformations() -> None:
    print("Starting Spark lakehouse transformations...")

    convert_all_raw_to_bronze()
    convert_all_bronze_to_silver()
    build_all_gold_datasets()

    print("Spark lakehouse transformations completed.")


if __name__ == "__main__":
    run_spark_lakehouse_transformations()