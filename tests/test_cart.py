from tests.conftest import client
from tests.conftest import TestingSessionLocal

from app.models.user import User
from app.models.category import Category


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

    token = login_response.json()["access_token"]

    db.close()

    return token


def create_product():

    db = TestingSessionLocal()

    category = db.query(Category).filter(
        Category.name == "Electronics"
    ).first()

    if not category:

        category = Category(
            name="Electronics"
        )

        db.add(category)

        db.commit()

        db.refresh(category)

    admin_token = get_admin_token()

    response = client.post(
        "/products",
        json={
            "name": "MacBook Pro",
            "description": "Laptop",
            "price": 2500,
            "stock": 10,
            "category_id": category.id
        },
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    db.close()

    return response.json()["id"]


def test_add_to_cart():

    product_id = create_product()

    token = get_customer_token()

    response = client.post(
        "/cart/add",
        json={
            "product_id": product_id,
            "quantity": 2
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == product_id
    assert data["quantity"] == 2


def test_get_cart():

    token = get_customer_token()

    response = client.get(
        "/cart",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_remove_cart_item():

    token = get_customer_token()

    cart_response = client.get(
        "/cart",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    cart_items = cart_response.json()

    if len(cart_items) == 0:
        return

    cart_item_id = cart_items[0]["id"]

    response = client.delete(
        f"/cart/{cart_item_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == "Item removed"