from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from schemas.attribute import AttributeResponse, AttributeCreate, AttributeUpdate
from models.attribute import Attribute

router = APIRouter(prefix="/attributes", tags=["Attributes"])

@router.get("/", response_model=list[AttributeResponse])
async def get_all_attributes(db: AsyncSession = Depends(get_db)):
    query = select(Attribute)
    result = await db.execute(query)
    attributes = result.scalars().all()
    return attributes

@router.post("/", response_model=AttributeResponse)
async def create_attribute(attribute: AttributeCreate, db: AsyncSession = Depends(get_db)):
    new_attribute = Attribute(name=attribute.name)
    db.add(new_attribute)
    await db.commit()
    await db.refresh(new_attribute)
    return new_attribute

@router.patch("/{attribute_id}", response_model=AttributeResponse)
async def update_attribute(
    attribute_id: int,
    attribute: AttributeUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(Attribute).where(Attribute.id == attribute_id)
    result = await db.execute(query)
    db_attribute = result.scalar_one_or_none()
    
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Атрибут не найден")
    
    if attribute.name is not None:
        db_attribute.name = attribute.name
    
    await db.commit()
    await db.refresh(db_attribute)
    return db_attribute

@router.delete("/{attribute_id}")
async def delete_attribute(attribute_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Attribute).where(Attribute.id == attribute_id)
    result = await db.execute(query)
    db_attribute = result.scalar_one_or_none()
    
    if not db_attribute:
        raise HTTPException(status_code=404, detail="Атрибут не найден")
    
    await db.delete(db_attribute)
    await db.commit()
    
    return {"message": "Атрибут удалён"}
