from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.category import Category    

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    query = select(Category)

    result = await db.excecute(query)
    # Убирает всю служебную обертку и оставляет только ORM-объекты, all() - возвращает все записи списком
    categories = result.scalars().all()

    return categories
