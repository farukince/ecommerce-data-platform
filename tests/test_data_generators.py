from apps.data_generator.generators.categories import generate_categories
from apps.data_generator.generators.events import (
    generate_cart_events,
    generate_click_events,
)
from apps.data_generator.generators.inventory import generate_product_inventory
from apps.data_generator.generators.orders import (
    generate_order_items,
    generate_orders,
    generate_payments,
    generate_returns,
    generate_shipments,
)
from apps.data_generator.generators.products import generate_products
from apps.data_generator.generators.sellers import generate_sellers
from apps.data_generator.generators.users import generate_users


def test_generate_categories_returns_expected_fields() -> None:
    categories = generate_categories()

    assert categories
    assert "category_name" in categories[0]


def test_generate_users_returns_expected_count() -> None:
    users = generate_users(count=5)

    assert len(users) == 5
    assert {"full_name", "email", "city"}.issubset(users[0].keys())


def test_generate_sellers_returns_expected_count() -> None:
    sellers = generate_sellers(count=3)

    assert len(sellers) == 3
    assert {"seller_name", "seller_city", "seller_score", "is_active"}.issubset(
        sellers[0].keys()
    )


def test_generate_products_returns_expected_fields() -> None:
    products = generate_products(category_ids=[1, 2], seller_ids=[10, 20], count=5)

    assert len(products) == 5
    assert {
        "seller_id",
        "category_id",
        "product_name",
        "brand",
        "price",
        "product_status",
    }.issubset(products[0].keys())


def test_generate_product_inventory_returns_one_row_per_product() -> None:
    inventory = generate_product_inventory(product_ids=[1, 2, 3])

    assert len(inventory) == 3
    assert {"product_id", "stock_quantity", "reserved_quantity"}.issubset(
        inventory[0].keys()
    )


def test_generate_orders_returns_expected_count() -> None:
    orders = generate_orders(user_ids=[1, 2, 3], count=5)

    assert len(orders) == 5
    assert {"user_id", "order_status", "order_date", "total_amount"}.issubset(
        orders[0].keys()
    )


def test_generate_order_items_returns_expected_count() -> None:
    order_items = generate_order_items(order_ids=[1, 2], product_ids=[10, 20], count=5)

    assert len(order_items) == 5
    assert {"order_id", "product_id", "quantity", "unit_price"}.issubset(
        order_items[0].keys()
    )


def test_generate_payments_returns_expected_fields() -> None:
    payments = generate_payments(order_ids=[1, 2, 3], count=2)

    assert len(payments) == 2
    assert {"order_id", "payment_status", "payment_method", "payment_amount"}.issubset(
        payments[0].keys()
    )


def test_generate_shipments_returns_expected_fields() -> None:
    shipments = generate_shipments(order_ids=[1, 2, 3], count=2)

    assert len(shipments) == 2
    assert {"order_id", "shipment_status", "cargo_company", "tracking_number"}.issubset(
        shipments[0].keys()
    )


def test_generate_returns_returns_expected_fields() -> None:
    returns = generate_returns(order_ids=[1, 2, 3], count=2)

    assert len(returns) == 2
    assert {"order_id", "return_reason", "return_status", "returned_at"}.issubset(
        returns[0].keys()
    )


def test_generate_click_events_returns_expected_count() -> None:
    events = generate_click_events(user_ids=[1, 2], product_ids=[10, 20], count=5)

    assert len(events) == 5
    assert {"user_id", "product_id", "event_type", "event_timestamp"}.issubset(
        events[0].keys()
    )


def test_generate_cart_events_returns_expected_count() -> None:
    events = generate_cart_events(user_ids=[1, 2], product_ids=[10, 20], count=5)

    assert len(events) == 5
    assert {"user_id", "product_id", "event_type", "quantity", "cart_id"}.issubset(
        events[0].keys()
    )
