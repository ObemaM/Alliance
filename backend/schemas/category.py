from pydantic import BaseModel

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: int | None
    
    class Config:
        from_attributes = True  # Позволяет создавать схему из ORM-модели
