from pydantic import BaseModel


class CartCreate(BaseModel):
    product_id: int
    quantity: int


class CartResponse(BaseModel):
    id: int
    quantity: int
    product_id: int
    user_id: int

    class Config:
        from_attributes = True