from pydantic import BaseModel


class AttributeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class AttributeCreate(BaseModel):
    name: str


class AttributeUpdate(BaseModel):
    name: str | None = None
