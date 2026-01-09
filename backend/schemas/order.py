from datetime import datetime
from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    customer_email: str | None
    delivery_address: str
    notes: str | None
    total_amount: float
    status: str

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: str | None = None
    delivery_address: str
    notes: str | None = None
    total_amount: float
    status: str = "new"


class OrderUpdate(BaseModel):
    customer_name: str | None = None
    customer_phone: str | None = None
    customer_email: str | None = None
    delivery_address: str | None = None
    notes: str | None = None
    total_amount: float | None = None
    status: str | None = None
