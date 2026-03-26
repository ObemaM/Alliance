from pydantic import BaseModel

from schemas.attribute import AttributeResponse


class ProductAttributeResponse(BaseModel):
    product_id: int
    attribute_id: int
    value_text: str | None
    attribute: AttributeResponse | None = None

    class Config:
        from_attributes = True


class ProductAttributeCreate(BaseModel):
    product_id: int
    attribute_id: int
    value_text: str | None = None


class ProductAttributeUpdate(BaseModel):
    product_id: int | None = None
    attribute_id: int | None = None
    value_text: str | None = None
