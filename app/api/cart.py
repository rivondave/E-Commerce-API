from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_user
)

from app.models.user import User
from app.models.product import Product
from app.models.cart_item import CartItem

from app.schemas.cart import (
    CartCreate,
    CartResponse
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.post(
    "/add",
    response_model=CartResponse
)
def add_to_cart(
    data: CartCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    product = (
        db.query(Product)
        .filter(
            Product.id
            == data.product_id
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if data.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    item = CartItem(
        quantity=data.quantity,
        user_id=current_user.id,
        product_id=data.product_id
    )

    db.add(item)

    db.commit()

    db.refresh(item)

    return item


@router.get(
    "",
    response_model=list[CartResponse]
)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return (
        db.query(CartItem)
        .filter(
            CartItem.user_id
            == current_user.id
        )
        .all()
    )

@router.delete(
    "/{cart_item_id}"
)
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    item = (
        db.query(CartItem)
        .filter(
            CartItem.id == cart_item_id,
            CartItem.user_id
            == current_user.id
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(item)

    db.commit()

    return {
        "message":
        "Item removed"
    }