from datetime import datetime
from typing import List

from pydantic import BaseModel
from schemas.category import CategoryNameResponse
from schemas.color import ColorResponse
from schemas.country import CountryResponse
from schemas.material import MaterialResponse
from schemas.product_attribute import ProductAttributeResponse
from schemas.product_image import ProductImageResponse

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    category_id: int | None
    pack_quantity: int | None
    quantity: int | None
    price: float | None
    weight: str | None
    color_id: int | None
    material_id: int | None
    country_id: int | None
    purpose: str | None
    created_at: datetime | None
    updated_at: datetime | None
    category: CategoryNameResponse | None = None
    color: ColorResponse | None = None
    material: MaterialResponse | None = None
    country: CountryResponse | None = None
    product_attributes: List[ProductAttributeResponse] = []
    images: List[ProductImageResponse] = []

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    category_id: int | None = None
    pack_quantity: int | None = None
    quantity: int | None = None
    price: float | None = None
    weight: str | None = None
    color_id: int | None = None
    material_id: int | None = None
    country_id: int | None = None
    purpose: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None
    pack_quantity: int | None = None
    quantity: int | None = None
    price: float | None = None
    weight: str | None = None
    color_id: int | None = None
    material_id: int | None = None
    country_id: int | None = None
    purpose: str | None = None
