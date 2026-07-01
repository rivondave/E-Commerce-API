from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float

    class Config:
        from_attributes = True