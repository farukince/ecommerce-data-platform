import random

from faker import Faker

fake = Faker("tr_TR")


BRANDS = [
    "TechNova",
    "ModaPlus",
    "Evora",
    "Sportiva",
    "CosmoLab",
    "BookLine",
    "Toymax",
    "FreshMarket",
]

PRODUCT_STATUSES = ["active", "active", "active", "inactive", "out_of_stock"]


def generate_products(
    category_ids: list[int],
    seller_ids: list[int],
    count: int = 200,
) -> list[dict]:
    products = []

    for _ in range(count):
        products.append(
            {
                "seller_id": random.choice(seller_ids),
                "category_id": random.choice(category_ids),
                "product_name": fake.word().title() + " " + fake.word().title(),
                "brand": random.choice(BRANDS),
                "price": round(random.uniform(50, 5000), 2),
                "product_status": random.choice(PRODUCT_STATUSES),
            }
        )

    return products