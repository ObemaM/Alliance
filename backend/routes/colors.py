from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.color import Color
from schemas.color import ColorResponse, ColorCreate, ColorUpdate

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

@router.post("/", response_model = ColorResponse)
async def create_color(color: ColorCreate, db: AsyncSession = Depends(get_db)):
    new_color = Color(name=color.name, code=color.code)
    db.add(new_color)
    await db.commit()
    await db.refresh(new_color)
    return new_color

@router.patch("/{color_id}", response_model=ColorResponse)
async def update_color(
    color_id: int, 
    color: ColorUpdate, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Color).where(Color.id == color_id)
    result = await db.execute(query)
    db_color = result.scalar_one_or_none()
    
    if not db_color:
        raise HTTPException(status_code=404, detail="Цвет не найден")
    
    if color.name is not None:
        db_color.name = color.name
    if color.code is not None:
        db_color.code = color.code
    
    await db.commit()
    await db.refresh(db_color)
    return db_color
    
@router.delete("/{color_id}")
async def delete_color(color_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Color).where(Color.id == color_id)
    result = await db.execute(query)
    db_color = result.scalar_one_or_none()

    if not db_color:
        raise HTTPException(status_code=404, detail="Цвет не найден")
    
    await db.delete(db_color)
    await db.commit()
    
    return {"message": "Цвет удален"}
