from pydantic import BaseModel

class MaterialResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # Позволяет создавать схему из ORM-модели

class MaterialCreate(BaseModel):
    name: str

class MaterialUpdate(BaseModel):
    name: str | None = None