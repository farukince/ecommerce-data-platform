from apps.data_generator.db import execute_many, fetch_ids, get_engine
from apps.data_generator.generators.categories import generate_categories
from apps.data_generator.generators.events import generate_cart_events, generate_click_events
from apps.data_generator.generators.orders import (
    generate_order_items,
    generate_orders,
    generate_payments,
    generate_returns,
    generate_shipments,
)
from apps.data_generator.generators.products import generate_products
from apps.data_generator.generators.users import generate_users


def insert_categories() -> None:
    engine = get_engine()
    rows = generate_categories()

    query = """
    INSERT INTO categories (category_name)
    VALUES (:category_name)
    ON CONFLICT (category_name) DO NOTHING
    """

    execute_many(engine, query, rows)
    print(f"Inserted categories: {len(rows)}")


def insert_users(count: int = 100) -> None:
    engine = get_engine()
    rows = generate_users(count)

    query = """
    INSERT INTO users (full_name, email, city)
    VALUES (:full_name, :email, :city)
    ON CONFLICT (email) DO NOTHING
    """

    execute_many(engine, query, rows)
    print(f"Inserted users: {len(rows)}")


def insert_products(count: int = 200) -> None:
    engine = get_engine()
    category_ids = fetch_ids(engine, "categories", "category_id")
    rows = generate_products(category_ids, count)

    query = """
    INSERT INTO products (category_id, product_name, brand, price)
    VALUES (:category_id, :product_name, :brand, :price)
    """

    execute_many(engine, query, rows)
    print(f"Inserted products: {len(rows)}")


def insert_orders(count: int = 300) -> None:
    engine = get_engine()
    user_ids = fetch_ids(engine, "users", "user_id")
    rows = generate_orders(user_ids, count)

    query = """
    INSERT INTO orders (user_id, order_status, order_date, total_amount, updated_at)
    VALUES (:user_id, :order_status, :order_date, :total_amount, :updated_at)
    """

    execute_many(engine, query, rows)
    print(f"Inserted orders: {len(rows)}")


def insert_order_items(count: int = 700) -> None:
    engine = get_engine()
    order_ids = fetch_ids(engine, "orders", "order_id")
    product_ids = fetch_ids(engine, "products", "product_id")
    rows = generate_order_items(order_ids, product_ids, count)

    query = """
    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    VALUES (:order_id, :product_id, :quantity, :unit_price)
    """

    execute_many(engine, query, rows)
    print(f"Inserted order_items: {len(rows)}")


def insert_payments(count: int = 300) -> None:
    engine = get_engine()
    order_ids = fetch_ids(engine, "orders", "order_id")
    rows = generate_payments(order_ids, count)

    query = """
    INSERT INTO payments (order_id, payment_status, payment_method, payment_amount, paid_at)
    VALUES (:order_id, :payment_status, :payment_method, :payment_amount, :paid_at)
    """

    execute_many(engine, query, rows)
    print(f"Inserted payments: {len(rows)}")


def insert_shipments(count: int = 250) -> None:
    engine = get_engine()
    order_ids = fetch_ids(engine, "orders", "order_id")
    rows = generate_shipments(order_ids, count)

    query = """
    INSERT INTO shipments (order_id, shipment_status, shipped_at, delivered_at)
    VALUES (:order_id, :shipment_status, :shipped_at, :delivered_at)
    """

    execute_many(engine, query, rows)
    print(f"Inserted shipments: {len(rows)}")


def insert_returns(count: int = 50) -> None:
    engine = get_engine()
    order_ids = fetch_ids(engine, "orders", "order_id")
    rows = generate_returns(order_ids, count)

    query = """
    INSERT INTO returns (order_id, return_reason, return_status, returned_at)
    VALUES (:order_id, :return_reason, :return_status, :returned_at)
    """

    execute_many(engine, query, rows)
    print(f"Inserted returns: {len(rows)}")


def insert_click_events(count: int = 1000) -> None:
    engine = get_engine()
    user_ids = fetch_ids(engine, "users", "user_id")
    product_ids = fetch_ids(engine, "products", "product_id")
    rows = generate_click_events(user_ids, product_ids, count)

    query = """
    INSERT INTO click_events (
        user_id, product_id, event_type, page_url, device_type, event_timestamp
    )
    VALUES (
        :user_id, :product_id, :event_type, :page_url, :device_type, :event_timestamp
    )
    """

    execute_many(engine, query, rows)
    print(f"Inserted click_events: {len(rows)}")


def insert_cart_events(count: int = 500) -> None:
    engine = get_engine()
    user_ids = fetch_ids(engine, "users", "user_id")
    product_ids = fetch_ids(engine, "products", "product_id")
    rows = generate_cart_events(user_ids, product_ids, count)

    query = """
    INSERT INTO cart_events (
        user_id, product_id, event_type, quantity, cart_id, event_timestamp
    )
    VALUES (
        :user_id, :product_id, :event_type, :quantity, :cart_id, :event_timestamp
    )
    """

    execute_many(engine, query, rows)
    print(f"Inserted cart_events: {len(rows)}")


def main() -> None:
    print("Starting synthetic ecommerce data generation...")

    insert_categories()
    insert_users()
    insert_products()
    insert_orders()
    insert_order_items()
    insert_payments()
    insert_shipments()
    insert_returns()
    insert_click_events()
    insert_cart_events()

    print("Synthetic ecommerce data generation completed.")


if __name__ == "__main__":
    main()