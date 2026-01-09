from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from models.category import Category    

router = APIRouter(prefix="/categories", tags=["Categories"])

# Depends для get запросов
@router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    query = select(Category)

    result = await db.execute(query)
    # Убирает всю служебную обертку и оставляет только ORM-объекты, all() - возвращает все записи списком
    categories = result.scalars().all()

    return categories

@router.post("/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    new_category = Category(
        name=category.name,
        slug=category.slug,
        parent_id=category.parent_id
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, 
    category: CategoryUpdate, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    db_category = result.scalar_one_or_none()
    
    if not db_category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    if category.name is not None:
        db_category.name = category.name
    if category.slug is not None:
        db_category.slug = category.slug
    if category.parent_id is not None:
        db_category.parent_id = category.parent_id
    
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Category).where(Category.id == category_id)
    result = await db.execute(query)
    db_category = result.scalar_one_or_none()
    
    if not db_category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    await db.delete(db_category)
    await db.commit()
    
    return {"message": "Категория удалена"}