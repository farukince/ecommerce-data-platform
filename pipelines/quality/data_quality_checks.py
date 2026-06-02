from dataclasses import dataclass
from pathlib import Path

import pandas as pd


SILVER_BASE_PATH = Path("data_lake/silver")


@dataclass
class QualityCheckResult:
    check_name: str
    table_name: str
    status: str
    failed_rows: int
    total_rows: int
    description: str

    def to_dict(self) -> dict:
        return {
            "check_name": self.check_name,
            "table_name": self.table_name,
            "status": self.status,
            "failed_rows": self.failed_rows,
            "total_rows": self.total_rows,
            "description": self.description,
        }


def read_silver_table(table_name: str) -> pd.DataFrame:
    input_path = SILVER_BASE_PATH / table_name / f"{table_name}.parquet"

    if not input_path.exists():
        raise FileNotFoundError(f"Silver file not found: {input_path}")

    return pd.read_parquet(input_path)


def build_result(
    check_name: str,
    table_name: str,
    failed_rows: int,
    total_rows: int,
    description: str,
) -> QualityCheckResult:
    return QualityCheckResult(
        check_name=check_name,
        table_name=table_name,
        status="passed" if failed_rows == 0 else "failed",
        failed_rows=int(failed_rows),
        total_rows=int(total_rows),
        description=description,
    )


def check_order_id_not_null() -> QualityCheckResult:
    orders = read_silver_table("orders")

    failed_rows = orders["order_id"].isna().sum()

    return build_result(
        check_name="order_id_not_null",
        table_name="orders",
        failed_rows=failed_rows,
        total_rows=len(orders),
        description="order_id must not be null.",
    )


def check_duplicate_orders() -> QualityCheckResult:
    orders = read_silver_table("orders")

    failed_rows = orders.duplicated(subset=["order_id"]).sum()

    return build_result(
        check_name="duplicate_orders",
        table_name="orders",
        failed_rows=failed_rows,
        total_rows=len(orders),
        description="order_id must be unique in orders table.",
    )


def check_payment_amount_non_negative() -> QualityCheckResult:
    payments = read_silver_table("payments")

    failed_rows = (payments["payment_amount"] < 0).sum()

    return build_result(
        check_name="payment_amount_non_negative",
        table_name="payments",
        failed_rows=failed_rows,
        total_rows=len(payments),
        description="payment_amount must be greater than or equal to zero.",
    )


def check_order_total_matches_items() -> QualityCheckResult:
    orders = read_silver_table("orders")
    order_items = read_silver_table("order_items")

    order_item_totals = order_items.copy()
    order_item_totals["line_amount"] = (
        order_item_totals["quantity"] * order_item_totals["unit_price"]
    )

    item_totals = (
        order_item_totals.groupby("order_id", as_index=False)
        .agg(items_total_amount=("line_amount", "sum"))
    )

    merged = orders.merge(item_totals, on="order_id", how="left")
    merged["items_total_amount"] = merged["items_total_amount"].fillna(0)

    tolerance = 0.01
    failed_rows = (
        (merged["total_amount"] - merged["items_total_amount"]).abs() > tolerance
    ).sum()

    return build_result(
        check_name="order_total_matches_order_items",
        table_name="orders",
        failed_rows=failed_rows,
        total_rows=len(orders),
        description="orders.total_amount should match sum(quantity * unit_price) from order_items.",
    )


def check_delivered_shipments_have_delivered_at() -> QualityCheckResult:
    shipments = read_silver_table("shipments")

    delivered_shipments = shipments["shipment_status"] == "delivered"
    missing_delivered_at = shipments["delivered_at"].isna()

    failed_rows = (delivered_shipments & missing_delivered_at).sum()

    return build_result(
        check_name="delivered_shipments_have_delivered_at",
        table_name="shipments",
        failed_rows=failed_rows,
        total_rows=len(shipments),
        description="Delivered shipments must have delivered_at timestamp.",
    )


def check_returns_have_valid_orders() -> QualityCheckResult:
    returns = read_silver_table("returns")
    orders = read_silver_table("orders")

    valid_order_ids = set(orders["order_id"].dropna().tolist())

    failed_rows = (~returns["order_id"].isin(valid_order_ids)).sum()

    return build_result(
        check_name="returns_have_valid_orders",
        table_name="returns",
        failed_rows=failed_rows,
        total_rows=len(returns),
        description="Every return record must reference an existing order_id.",
    )


def check_event_timestamp_not_in_future() -> list[QualityCheckResult]:
    results = []
    now = pd.Timestamp.now()

    for table_name in ["click_events", "cart_events"]:
        events = read_silver_table(table_name)

        event_timestamps = pd.to_datetime(events["event_timestamp"], errors="coerce")
        failed_rows = (event_timestamps > now).sum()

        results.append(
            build_result(
                check_name="event_timestamp_not_in_future",
                table_name=table_name,
                failed_rows=failed_rows,
                total_rows=len(events),
                description="Event timestamp must not be in the future.",
            )
        )

    return results


def run_all_quality_checks() -> list[QualityCheckResult]:
    results = [
        check_order_id_not_null(),
        check_duplicate_orders(),
        check_payment_amount_non_negative(),
        check_order_total_matches_items(),
        check_delivered_shipments_have_delivered_at(),
        check_returns_have_valid_orders(),
    ]

    results.extend(check_event_timestamp_not_in_future())

    return results