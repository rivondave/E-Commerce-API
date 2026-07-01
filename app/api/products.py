from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.product import Product
from app.models.category import Category

from app.schemas.product import (
    ProductCreate,
    ProductResponse
)

from app.core.admin import (
    admin_required
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post(
    "",
    response_model=ProductResponse
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        admin_required
    )
):

    category = (
        db.query(Category)
        .filter(
            Category.id
            == data.category_id
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    product = Product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        category_id=data.category_id
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return product


@router.get(
    "",
    response_model=list[ProductResponse]
)
def get_products(
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Product)

    if search:
        query = query.filter(
            Product.name.ilike(
                f"%{search}%"
            )
        )

    if min_price:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price:
        query = query.filter(
            Product.price <= max_price
        )

    if category_id:
        query = query.filter(
            Product.category_id
            == category_id
        )

    return query.all()


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(
            Product.id
            == product_id
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        admin_required
    )
):

    product = (
        db.query(Product)
        .filter(
            Product.id == product_id
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.name = data.name
    product.description = data.description
    product.price = data.price
    product.stock = data.stock
    product.category_id = data.category_id

    db.commit()

    db.refresh(product)

    return product

@router.delete(
    "/{product_id}"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        admin_required
    )
):

    product = (
        db.query(Product)
        .filter(
            Product.id == product_id
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)

    db.commit()

    return {
        "message":
        "Product deleted"
    }