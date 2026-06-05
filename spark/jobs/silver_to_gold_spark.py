from pathlib import Path

from pyspark.sql.functions import (
    avg,
    col,
    count,
    countDistinct,
    lit,
    round,
    sum,
    to_date,
    when,
)

from spark.utils.spark_session import get_spark_session


SILVER_BASE_PATH = Path("data_lake/silver")
GOLD_BASE_PATH = Path("data_lake/gold")


def read_silver_table(table_name: str):
    spark = get_spark_session("silver-to-gold-spark")
    input_path = SILVER_BASE_PATH / table_name

    return spark.read.parquet(str(input_path))


def write_gold_dataset(dataset_name: str, df) -> None:
    output_path = GOLD_BASE_PATH / dataset_name
    df.write.mode("overwrite").parquet(str(output_path))

    print(f"Spark gold created | dataset={dataset_name} | output={output_path}")


def build_daily_sales() -> None:
    orders = read_silver_table("orders")

    daily_sales = (
        orders.withColumn("order_day", to_date(col("order_date")))
        .groupBy("order_day")
        .agg(
            countDistinct("order_id").alias("order_count"),
            sum("total_amount").alias("total_revenue"),
            round(avg("total_amount"), 2).alias("average_order_value"),
        )
        .orderBy("order_day")
    )

    write_gold_dataset("gold_daily_sales_spark", daily_sales)


def build_category_sales() -> None:
    order_items = read_silver_table("order_items")
    products = read_silver_table("products")
    categories = read_silver_table("categories")

    merged = (
        order_items.join(products, on="product_id", how="left")
        .join(categories, on="category_id", how="left")
        .withColumn("line_amount", col("quantity") * col("unit_price"))
    )

    category_sales = (
        merged.groupBy("category_name")
        .agg(
            sum("quantity").alias("sold_quantity"),
            sum("line_amount").alias("total_revenue"),
            countDistinct("product_id").alias("unique_products"),
        )
        .orderBy(col("total_revenue").desc())
    )

    write_gold_dataset("gold_category_sales_spark", category_sales)


def build_payment_summary() -> None:
    payments = read_silver_table("payments")

    payment_summary = (
        payments.groupBy("payment_status", "payment_method")
        .agg(
            countDistinct("payment_id").alias("payment_count"),
            sum("payment_amount").alias("total_payment_amount"),
            round(avg("payment_amount"), 2).alias("average_payment_amount"),
        )
        .orderBy(col("payment_count").desc())
    )

    write_gold_dataset("gold_payment_summary_spark", payment_summary)


def build_conversion_funnel() -> None:
    click_events = read_silver_table("click_events")
    cart_events = read_silver_table("cart_events")
    orders = read_silver_table("orders")

    spark = get_spark_session("silver-to-gold-spark")

    product_views = (
        click_events
        .filter(col("event_type") == "product_viewed")
        .select("user_id")
        .distinct()
        .count()
    )

    cart_adds = (
        cart_events
        .filter(col("event_type") == "product_added_to_cart")
        .select("user_id")
        .distinct()
        .count()
    )

    purchasers = orders.select("user_id").distinct().count()

    funnel_rows = [
        ("product_viewed", product_views),
        ("product_added_to_cart", cart_adds),
        ("order_created", purchasers),
    ]

    funnel = spark.createDataFrame(
        funnel_rows,
        ["step", "unique_users"],
    )

    funnel = funnel.withColumn(
        "step_order",
        when(col("step") == "product_viewed", lit(1))
        .when(col("step") == "product_added_to_cart", lit(2))
        .when(col("step") == "order_created", lit(3)),
    ).orderBy("step_order")

    write_gold_dataset("gold_conversion_funnel_spark", funnel)


def build_all_gold_datasets() -> None:
    print("Starting Spark silver to gold transformation...")

    build_daily_sales()
    build_category_sales()
    build_payment_summary()
    build_conversion_funnel()

    print("Spark silver to gold transformation completed.")


if __name__ == "__main__":
    build_all_gold_datasets()