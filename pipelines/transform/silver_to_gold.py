from pathlib import Path

import pandas as pd


SILVER_BASE_PATH = Path("data_lake/silver")
GOLD_BASE_PATH = Path("data_lake/gold")


def read_silver_table(table_name: str) -> pd.DataFrame:
    input_path = SILVER_BASE_PATH / table_name / f"{table_name}.parquet"

    if not input_path.exists():
        raise FileNotFoundError(f"Silver file not found: {input_path}")

    return pd.read_parquet(input_path)


def write_gold_dataset(dataset_name: str, df: pd.DataFrame) -> Path:
    output_dir = GOLD_BASE_PATH / dataset_name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{dataset_name}.json"
    df.to_json(output_path, orient="records", force_ascii=False, indent=2, date_format="iso")

    print(
        f"Gold created | dataset={dataset_name} | rows={len(df)} | output={output_path}"
    )

    return output_path


def build_daily_sales() -> Path:
    orders = read_silver_table("orders")

    orders["order_day"] = pd.to_datetime(orders["order_date"]).dt.date

    daily_sales = (
        orders.groupby("order_day", as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            total_revenue=("total_amount", "sum"),
            average_order_value=("total_amount", "mean"),
        )
        .sort_values("order_day")
    )

    return write_gold_dataset("gold_daily_sales", daily_sales)


def build_category_sales() -> Path:
    order_items = read_silver_table("order_items")
    products = read_silver_table("products")
    categories = read_silver_table("categories")

    merged = (
        order_items.merge(products, on="product_id", how="left")
        .merge(categories, on="category_id", how="left")
    )

    merged["line_amount"] = merged["quantity"] * merged["unit_price"]

    category_sales = (
        merged.groupby("category_name", as_index=False)
        .agg(
            sold_quantity=("quantity", "sum"),
            total_revenue=("line_amount", "sum"),
            unique_products=("product_id", "nunique"),
        )
        .sort_values("total_revenue", ascending=False)
    )

    return write_gold_dataset("gold_category_sales", category_sales)


def build_payment_summary() -> Path:
    payments = read_silver_table("payments")

    payment_summary = (
        payments.groupby(["payment_status", "payment_method"], as_index=False)
        .agg(
            payment_count=("payment_id", "nunique"),
            total_payment_amount=("payment_amount", "sum"),
            average_payment_amount=("payment_amount", "mean"),
        )
        .sort_values("payment_count", ascending=False)
    )

    return write_gold_dataset("gold_payment_summary", payment_summary)


def build_conversion_funnel() -> Path:
    click_events = read_silver_table("click_events")
    cart_events = read_silver_table("cart_events")
    orders = read_silver_table("orders")

    product_views = click_events[
        click_events["event_type"] == "product_viewed"
    ]["user_id"].nunique()

    cart_adds = cart_events[
        cart_events["event_type"] == "product_added_to_cart"
    ]["user_id"].nunique()

    purchasers = orders["user_id"].nunique()

    funnel = pd.DataFrame(
        [
            {
                "step": "product_viewed",
                "unique_users": product_views,
            },
            {
                "step": "product_added_to_cart",
                "unique_users": cart_adds,
            },
            {
                "step": "order_created",
                "unique_users": purchasers,
            },
        ]
    )

    funnel["previous_step_users"] = funnel["unique_users"].shift(1)
    funnel["conversion_rate_from_previous_step"] = (
        funnel["unique_users"] / funnel["previous_step_users"]
    ).fillna(1.0)

    return write_gold_dataset("gold_conversion_funnel", funnel)


def build_all_gold_datasets() -> None:
    print("Starting silver to gold transformation...")

    build_daily_sales()
    build_category_sales()
    build_payment_summary()
    build_conversion_funnel()

    print("Silver to gold transformation completed.")