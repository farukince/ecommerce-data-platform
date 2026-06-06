import random

from faker import Faker

fake = Faker("tr_TR")


def generate_sellers(count: int = 30) -> list[dict]:
    sellers = []

    for _ in range(count):
        sellers.append(
            {
                "seller_name": fake.company(),
                "seller_city": fake.city(),
                "seller_score": round(random.uniform(3.0, 5.0), 2),
                "is_active": random.choice([True, True, True, False]),
            }
        )

    return sellers
