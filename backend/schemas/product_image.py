# pydantic - для создания схем
from pydantic import BaseModel

class ProductImageResponse(BaseModel):
    id: int
    product_id: int
    url: str | None

    class Config:
        from_attributes = True  # Позволяет создавать схему из ORM-модели

class ProductImageCreate(BaseModel):
    product_id: int
    url: str | None

class ProductImageUpdate(BaseModel):
    product_id: int | None = None
    url: str | None = None