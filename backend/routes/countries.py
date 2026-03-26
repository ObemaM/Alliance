from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.country import Country
from models.product import Product
from schemas.country import CountryResponse, CountryCreate, CountryUpdate

# URL будут начинаться с /countries и будут относиться тегу (в документации) Countries
router = APIRouter(prefix="/countries", tags=["Countries"])

@router.get("/available", response_model=list[CountryResponse])
async def get_available_countries(db: AsyncSession = Depends(get_db)):
    query = select(Country).join(Product, Country.id == Product.country_id).distinct()

    result = await db.execute(query)
    countries = result.scalars().all()

    return countries

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

@router.post("/", response_model=CountryResponse)
async def create_country(country: CountryCreate, db: AsyncSession = Depends(get_db)):
    new_country = Country(name=country.name)
    db.add(new_country)
    await db.commit()
    await db.refresh(new_country)
    return new_country

@router.patch("/{country_id}", response_model=CountryResponse)
async def update_country(
    country_id: int, 
    country: CountryUpdate, 
    db: AsyncSession = Depends(get_db)
):
    query = select(Country).where(Country.id == country_id)
    result = await db.execute(query)
    db_country = result.scalar_one_or_none()
    
    if not db_country:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    
    if country.name is not None:
        db_country.name = country.name
    
    await db.commit()
    await db.refresh(db_country)
    return db_country

@router.delete("/{country_id}")
async def delete_country(country_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Country).where(Country.id == country_id)
    result = await db.execute(query)
    db_country = result.scalar_one_or_none()
    
    if not db_country:
        raise HTTPException(status_code=404, detail="Страна не найдена")
    
    await db.delete(db_country)
    await db.commit()
    
    return {"message": "Страна удалена"}
