from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from schemas.product_attribute import ProductAttributeResponse, ProductAttributeCreate, ProductAttributeUpdate
from models.product_attribute import ProductAttribute

router = APIRouter(prefix="/product_attributes", tags=["Product Attributes"])

@router.get("/", response_model=list[ProductAttributeResponse])
async def get_all_product_attributes(db: AsyncSession = Depends(get_db)):
    query = select(ProductAttribute)
    result = await db.execute(query)
    attrs = result.scalars().all()
    return attrs

@router.get("/product/{product_id}", response_model=list[ProductAttributeResponse])
async def get_attributes_by_product(product_id: int, db: AsyncSession = Depends(get_db)):
    query = select(ProductAttribute).where(ProductAttribute.product_id == product_id)
    result = await db.execute(query)
    attrs = result.scalars().all()
    return attrs

@router.post("/", response_model=ProductAttributeResponse)
async def create_product_attribute(attr: ProductAttributeCreate, db: AsyncSession = Depends(get_db)):
    new_attr = ProductAttribute(
        product_id=attr.product_id,
        attribute_id=attr.attribute_id,
        value_text=attr.value_text
    )
    db.add(new_attr)
    await db.commit()
    await db.refresh(new_attr)
    return new_attr

@router.patch("/{product_id}/{attribute_id}", response_model=ProductAttributeResponse)
async def update_product_attribute(
    product_id: int,
    attribute_id: int,
    attr: ProductAttributeUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(ProductAttribute).where(
        ProductAttribute.product_id == product_id,
        ProductAttribute.attribute_id == attribute_id
    )
    result = await db.execute(query)
    db_attr = result.scalar_one_or_none()
    
    if not db_attr:
        raise HTTPException(status_code=404, detail="Атрибут товара не найден")
    
    if attr.product_id is not None:
        db_attr.product_id = attr.product_id
    if attr.attribute_id is not None:
        db_attr.attribute_id = attr.attribute_id
    if attr.value_text is not None:
        db_attr.value_text = attr.value_text
    
    await db.commit()
    await db.refresh(db_attr)
    return db_attr

@router.delete("/{product_id}/{attribute_id}")
async def delete_product_attribute(
    product_id: int,
    attribute_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = select(ProductAttribute).where(
        ProductAttribute.product_id == product_id,
        ProductAttribute.attribute_id == attribute_id
    )
    result = await db.execute(query)
    db_attr = result.scalar_one_or_none()
    
    if not db_attr:
        raise HTTPException(status_code=404, detail="Атрибут товара не найден")
    
    await db.delete(db_attr)
    await db.commit()
    
    return {"message": "Атрибут товара удалён"}
