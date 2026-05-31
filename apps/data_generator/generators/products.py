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


def generate_products(category_ids: list[int], count: int = 200) -> list[dict]:
    products = []

    for _ in range(count):
        products.append(
            {
                "category_id": random.choice(category_ids),
                "product_name": fake.word().title() + " " + fake.word().title(),
                "brand": random.choice(BRANDS),
                "price": round(random.uniform(50, 5000), 2),
            }
        )

    return products