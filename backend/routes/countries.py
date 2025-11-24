from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.country import Country
from schemas.country import CountryResponse

# URL будут начинаться с /countries и будут относиться тегу (в документации) Countries
router = APIRouter(prefix="/countries", tags=["Countries"])

# Список элементов CountryResponse - list[CountryResponse]
# Выбираем по какому эндпоинту надо обращаться
@router.get("/", response_model=list[CountryResponse])
async def get_all_countries(db: AsyncSession = Depends(get_db)):
    # Создаем запрос для выбора всех стран
    query = select(Country)
    
    # Выполняем запрос асинхронно
    result = await db.execute(query)
    
    # Получаем все записи
    countries = result.scalars().all()
    
    return countries
