from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.material import Material
from schemas.material import MaterialResponse
from schemas.material import MaterialCreate
from schemas.material import MaterialUpdate

router = APIRouter(prefix="/materials", tags=["Materials"])

@router.get("/", response_model=list[MaterialResponse])
async def get_all_materials(db: AsyncSession = Depends(get_db)):
    query = select(Material)
    result = await db.execute(query)
    materials = result.scalars().all()
    return materials

@router.post("/", response_model=MaterialResponse)
async def create_material(material: MaterialCreate, db: AsyncSession = Depends(get_db)):
    new_material = Material(name=material.name)
    db.add(new_material)
    await db.commit()
    await db.refresh(new_material)
    return new_material

@router.patch("/{material_id}", response_model=MaterialResponse)
async def update_material(
    material_id: int, 
    material: MaterialUpdate, 
    db: AsyncSession = Depends(get_db)
):
    # Находим материал в БД
    query = select(Material).where(Material.id == material_id)
    result = await db.execute(query)
    db_material = result.scalar_one_or_none()
    
    if not db_material:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Материал не найден")
    
    # Обновляем только те поля, которые пришли в запросе
    if material.name is not None:
        db_material.name = material.name
    
    await db.commit()
    await db.refresh(db_material)
    return db_material

# Удалению не нужно тело запроса в schemas
@router.delete("/{material_id}")
async def delete_material(material_id: int, db: AsyncSession = Depends(get_db)):
    # Находим материал в БД
    query = select(Material).where(Material.id == material_id)
    result = await db.execute(query)
    db_material = result.scalar_one_or_none()
    
    if not db_material:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Материал не найден")
    
    await db.delete(db_material)
    await db.commit()
    
    return {"message": "Материал удален"}