import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker("tr_TR")


ORDER_STATUSES = ["created", "paid", "packed", "shipped", "delivered", "cancelled"]
PAYMENT_STATUSES = ["success", "failed", "refunded"]
PAYMENT_METHODS = ["credit_card", "debit_card", "wallet", "bank_transfer"]
SHIPMENT_STATUSES = ["preparing", "shipped", "delivered", "delayed"]
RETURN_STATUSES = ["requested", "approved", "rejected", "completed"]
RETURN_REASONS = ["damaged_product", "wrong_size", "late_delivery", "changed_mind"]


def random_datetime_within_days(days: int = 30) -> datetime:
    return datetime.now() - timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )


def generate_orders(user_ids: list[int], count: int = 300) -> list[dict]:
    orders = []

    for _ in range(count):
        order_date = random_datetime_within_days()
        total_amount = round(random.uniform(100, 15000), 2)

        orders.append(
            {
                "user_id": random.choice(user_ids),
                "order_status": random.choice(ORDER_STATUSES),
                "order_date": order_date,
                "total_amount": total_amount,
                "updated_at": order_date,
            }
        )

    return orders


def generate_order_items(order_ids: list[int], product_ids: list[int], count: int = 700) -> list[dict]:
    order_items = []

    for _ in range(count):
        quantity = random.randint(1, 4)
        unit_price = round(random.uniform(50, 5000), 2)

        order_items.append(
            {
                "order_id": random.choice(order_ids),
                "product_id": random.choice(product_ids),
                "quantity": quantity,
                "unit_price": unit_price,
            }
        )

    return order_items


def generate_payments(order_ids: list[int], count: int = 300) -> list[dict]:
    payments = []

    for order_id in random.sample(order_ids, min(count, len(order_ids))):
        payment_status = random.choice(PAYMENT_STATUSES)

        payments.append(
            {
                "order_id": order_id,
                "payment_status": payment_status,
                "payment_method": random.choice(PAYMENT_METHODS),
                "payment_amount": round(random.uniform(100, 15000), 2),
                "paid_at": random_datetime_within_days() if payment_status == "success" else None,
            }
        )

    return payments


def generate_shipments(order_ids: list[int], count: int = 250) -> list[dict]:
    shipments = []

    for order_id in random.sample(order_ids, min(count, len(order_ids))):
        shipment_status = random.choice(SHIPMENT_STATUSES)
        shipped_at = random_datetime_within_days()
        delivered_at = shipped_at + timedelta(days=random.randint(1, 7)) if shipment_status == "delivered" else None

        shipments.append(
            {
                "order_id": order_id,
                "shipment_status": shipment_status,
                "shipped_at": shipped_at,
                "delivered_at": delivered_at,
            }
        )

    return shipments


def generate_returns(order_ids: list[int], count: int = 50) -> list[dict]:
    returns = []

    for order_id in random.sample(order_ids, min(count, len(order_ids))):
        returns.append(
            {
                "order_id": order_id,
                "return_reason": random.choice(RETURN_REASONS),
                "return_status": random.choice(RETURN_STATUSES),
                "returned_at": random_datetime_within_days(),
            }
        )

    return returns