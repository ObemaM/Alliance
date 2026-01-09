from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    product_id: int
    order_id: int
    quantity: int
    price_at_purchase: float | None

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    order_id: int
    quantity: int
    price_at_purchase: float | None = None


class OrderItemUpdate(BaseModel):
    product_id: int | None = None
    order_id: int | None = None
    quantity: int | None = None
    price_at_purchase: float | None = None
