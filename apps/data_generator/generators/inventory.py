import random

from faker import Faker

fake = Faker("tr_TR")


def generate_product_inventory(product_ids: list[int]) -> list[dict]:
    inventory_rows = []

    for product_id in product_ids:
        stock_quantity = random.randint(0, 500)
        reserved_quantity = random.randint(0, min(stock_quantity, 50))

        inventory_rows.append(
            {
                "product_id": product_id,
                "stock_quantity": stock_quantity,
                "reserved_quantity": reserved_quantity,
                "warehouse_location": random.choice(
                    ["Istanbul", "Ankara", "Izmir", "Kocaeli", "Bursa"]
                ),
            }
        )

    return inventory_rows