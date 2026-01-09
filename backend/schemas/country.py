from pydantic import BaseModel

class CountryResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True  # Позволяет создавать схему из ORM-модели

class CountryCreate(BaseModel):
    name: str

class CountryUpdate(BaseModel):
    name: str | None = None
