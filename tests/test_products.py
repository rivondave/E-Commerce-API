from tests.conftest import client

from app.models.user import User
from app.models.category import Category

from tests.conftest import TestingSessionLocal


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


def create_category():

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

    category_id = category.id

    db.close()

    return category_id


def test_create_product():

    token = get_admin_token()

    category_id = create_category()

    response = client.post(
        "/products",
        json={
            "name": "iPhone 15",
            "description": "Apple smartphone",
            "price": 999.99,
            "stock": 10,
            "category_id": category_id
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "iPhone 15"


def test_get_products():

    response = client.get("/products")

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_get_single_product():

    response = client.get(
        "/products/1"
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data