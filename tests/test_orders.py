from tests.conftest import client
from tests.conftest import TestingSessionLocal

from app.models.user import User
from app.models.category import Category


def get_admin_token():

    db = TestingSessionLocal()

    user = db.query(User).filter(
        User.email == "admin@test.com"
    ).first()

    if not user:

        client.post(
            "/auth/register",
            json={
                "email": "admin@test.com",
                "password": "password123"
            }
        )

        user = db.query(User).filter(
            User.email == "admin@test.com"
        ).first()

        user.role = "admin"

        db.commit()

    login_response = client.post(
        "/auth/login",
        data={
            "username": "admin@test.com",
            "password": "password123"
        }
    )

    db.close()

    return login_response.json()["access_token"]


def get_customer_token():

    db = TestingSessionLocal()

    user = db.query(User).filter(
        User.email == "customer@test.com"
    ).first()

    if not user:

        client.post(
            "/auth/register",
            json={
                "email": "customer@test.com",
                "password": "password123"
            }
        )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "customer@test.com",
            "password": "password123"
        }
    )

    db.close()

    return login_response.json()["access_token"]


def create_product_for_checkout():

    db = TestingSessionLocal()

    category = db.query(Category).filter(
        Category.name == "Checkout Category"
    ).first()

    if not category:

        category = Category(
            name="Checkout Category"
        )

        db.add(category)

        db.commit()

        db.refresh(category)

    admin_token = get_admin_token()

    response = client.post(
        "/products",
        json={
            "name": "Checkout Product",
            "description": "Order Test Product",
            "price": 100,
            "stock": 20,
            "category_id": category.id
        },
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    db.close()

    return response.json()["id"]


def prepare_cart():

    product_id = create_product_for_checkout()

    customer_token = get_customer_token()

    client.post(
        "/cart/add",
        json={
            "product_id": product_id,
            "quantity": 2
        },
        headers={
            "Authorization": f"Bearer {customer_token}"
        }
    )

    return customer_token


def test_checkout():

    token = prepare_cart()

    response = client.post(
        "/orders/checkout",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["total_amount"] > 0


def test_get_orders():

    token = prepare_cart()

    client.post(
        "/orders/checkout",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(
        "/orders",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    orders = response.json()

    assert isinstance(orders, list)
    assert len(orders) > 0


def test_get_single_order():

    token = prepare_cart()

    checkout_response = client.post(
        "/orders/checkout",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    order_id = checkout_response.json()["id"]

    response = client.get(
        f"/orders/{order_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == order_id