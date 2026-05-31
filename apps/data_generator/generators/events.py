import random
from datetime import datetime, timedelta

from faker import Faker

fake = Faker("tr_TR")


CLICK_EVENT_TYPES = [
    "homepage_viewed",
    "category_viewed",
    "product_viewed",
    "search_performed",
    "product_favorited",
]

CART_EVENT_TYPES = [
    "cart_created",
    "product_added_to_cart",
    "product_removed_from_cart",
    "cart_quantity_updated",
    "checkout_started",
]

DEVICE_TYPES = ["mobile", "desktop", "tablet"]


def random_event_timestamp(days: int = 30) -> datetime:
    return datetime.now() - timedelta(
        days=random.randint(0, days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )


def generate_click_events(
    user_ids: list[int],
    product_ids: list[int],
    count: int = 1000,
) -> list[dict]:
    events = []

    for _ in range(count):
        events.append(
            {
                "user_id": random.choice(user_ids),
                "product_id": random.choice(product_ids),
                "event_type": random.choice(CLICK_EVENT_TYPES),
                "page_url": fake.uri_path(),
                "device_type": random.choice(DEVICE_TYPES),
                "event_timestamp": random_event_timestamp(),
            }
        )

    return events


def generate_cart_events(
    user_ids: list[int],
    product_ids: list[int],
    count: int = 500,
) -> list[dict]:
    events = []

    for _ in range(count):
        events.append(
            {
                "user_id": random.choice(user_ids),
                "product_id": random.choice(product_ids),
                "event_type": random.choice(CART_EVENT_TYPES),
                "quantity": random.randint(1, 5),
                "cart_id": fake.uuid4(),
                "event_timestamp": random_event_timestamp(),
            }
        )

    return events