import random
from datetime import datetime
from uuid import uuid4

from faker import Faker

fake = Faker("tr_TR")


DEVICE_TYPES = ["mobile", "desktop", "tablet"]
PAYMENT_METHODS = ["credit_card", "debit_card", "wallet", "bank_transfer"]
PAYMENT_STATUSES = ["success", "failed"]
ORDER_STATUSES = ["created", "paid", "cancelled"]


def base_event(event_type: str) -> dict:
    return {
        "event_id": str(uuid4()),
        "event_type": event_type,
        "event_timestamp": datetime.now().isoformat(),
        "user_id": random.randint(1, 100),
        "session_id": str(uuid4()),
        "source": "kafka_stream",
    }


def build_product_viewed_event() -> dict:
    event = base_event("product_viewed")
    event.update(
        {
            "product_id": random.randint(1, 200),
            "device_type": random.choice(DEVICE_TYPES),
            "page_url": fake.uri_path(),
        }
    )
    return event


def build_cart_updated_event() -> dict:
    event = base_event("cart_updated")
    event.update(
        {
            "cart_id": str(uuid4()),
            "product_id": random.randint(1, 200),
            "quantity": random.randint(1, 5),
            "cart_action": random.choice(
                [
                    "product_added_to_cart",
                    "product_removed_from_cart",
                    "cart_quantity_updated",
                ]
            ),
        }
    )
    return event


def build_order_created_event() -> dict:
    event = base_event("order_created")
    event.update(
        {
            "order_id": random.randint(1, 100000),
            "order_status": random.choice(ORDER_STATUSES),
            "total_amount": round(random.uniform(100, 15000), 2),
        }
    )
    return event


def build_payment_completed_event() -> dict:
    event = base_event("payment_completed")
    event.update(
        {
            "payment_id": random.randint(1, 100000),
            "order_id": random.randint(1, 100000),
            "payment_method": random.choice(PAYMENT_METHODS),
            "payment_status": random.choice(PAYMENT_STATUSES),
            "payment_amount": round(random.uniform(100, 15000), 2),
        }
    )
    return event


def build_event_for_topic(topic: str) -> dict:
    if topic == "product_viewed":
        return build_product_viewed_event()

    if topic == "cart_updated":
        return build_cart_updated_event()

    if topic == "order_created":
        return build_order_created_event()

    if topic == "payment_completed":
        return build_payment_completed_event()

    raise ValueError(f"Unsupported Kafka topic: {topic}")
