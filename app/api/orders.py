from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_user
)

from app.models.user import User
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

from app.schemas.order import (
    OrderResponse
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post(
    "/checkout",
    response_model=OrderResponse
)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    cart_items = (
        db.query(CartItem)
        .filter(
            CartItem.user_id
            == current_user.id
        )
        .all()
    )

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total_amount = 0

    for item in cart_items:

        product = (
            db.query(Product)
            .filter(
                Product.id
                == item.product_id
            )
            .first()
        )

        if item.quantity > product.stock:

            raise HTTPException(
                status_code=400,
                detail=f"{product.name} out of stock"
            )

        total_amount += (
            product.price
            * item.quantity
        )

    order = Order(
        user_id=current_user.id,
        total_amount=total_amount
    )

    db.add(order)

    db.commit()

    db.refresh(order)

    for item in cart_items:

        product = (
            db.query(Product)
            .filter(
                Product.id
                == item.product_id
            )
            .first()
        )

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price
        )

        db.add(order_item)

        product.stock -= item.quantity

        db.delete(item)

    db.commit()

    return order


@router.get(
    "",
    response_model=list[OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return (
        db.query(Order)
        .filter(
            Order.user_id
            == current_user.id
        )
        .all()
    )

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id
            == current_user.id
        )
        .first()
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order