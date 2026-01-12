from pydantic import BaseModel

class ColorResponse(BaseModel):
    id: int
    name: str
    code: str | None
    
    class Config:
        from_attributes = True  # Позволяет создавать схему из ORM-модели

class ColorCreate(BaseModel):
    name: str
    code: str | None = None

class ColorUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
