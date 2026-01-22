from pydantic import BaseModel

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: int | None
    
    class Config:
        from_attributes = True  # Позволяет создавать схему из ORM-модели
    
class CategoryNameResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

# Создание
class CategoryCreate(BaseModel):
    name: str
    slug: str
    parent_id: int | None = None


# Редактирование - в update все поля не обязательны
class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    parent_id: int | None = None
