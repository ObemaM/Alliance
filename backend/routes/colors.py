from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.color import Color
from schemas.color import ColorResponse

router = APIRouter(prefix="/colors", tags=["Colors"])

@router.get("/", response_model=list[ColorResponse])
async def get_all_colors(db: AsyncSession = Depends(get_db)):
    # Создаем запрос для выбора всех цветов
    query = select(Color)
    
    # Выполняем запрос асинхронно
    result = await db.execute(query)
    
    # Получаем все записи
    colors = result.scalars().all()
    
    return colors
