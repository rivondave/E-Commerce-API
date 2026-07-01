from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.cart_item import CartItem

from app.core.database import (
    Base,
    engine
)

from app.api.categories import (
    router as category_router
)

from app.api.products import (
    router as product_router
)

from app.api.cart import (
    router as cart_router
)

from app.api.orders import (
    router as orders_router
)

from app.models.order import Order
from app.models.order_item import OrderItem


Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="E-Commerce Backend API (rivondave)",
    version="1.0.0"
)


app.include_router(cart_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(orders_router)


@app.get("/")
def root():
    return {
        "message": "E-Commerce API Running"
    }

