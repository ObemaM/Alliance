from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from schemas.product_image import ProductImageResponse, ProductImageCreate, ProductImageUpdate
from models.product_image import ProductImage

router = APIRouter(prefix="/product_images", tags=["Product Images"])

@router.get("/", response_model=list[ProductImageResponse])
async def get_all_product_images(db: AsyncSession = Depends(get_db)):
    query = select(ProductImage)
    result = await db.execute(query)
    product_images = result.scalars().all()
    return product_images

@router.post("/", response_model=ProductImageResponse)
async def create_product_image(product_image: ProductImageCreate, db: AsyncSession = Depends(get_db)):
    new_product_image = ProductImage(
        product_id=product_image.product_id,
        url=product_image.url
    )
    db.add(new_product_image)
    await db.commit()
    await db.refresh(new_product_image)
    return new_product_image

@router.patch("/{product_image_id}", response_model=ProductImageResponse)
async def update_product_image(
    product_image_id: int, 
    product_image: ProductImageUpdate, 
    db: AsyncSession = Depends(get_db)
):
    query = select(ProductImage).where(ProductImage.id == product_image_id)
    result = await db.execute(query)
    db_product_image = result.scalar_one_or_none()
    
    if not db_product_image:
        raise HTTPException(status_code=404, detail="Изображение товара не найдено")
    
    if product_image.product_id is not None:
        db_product_image.product_id = product_image.product_id
    if product_image.url is not None:
        db_product_image.url = product_image.url
    
    await db.commit()
    await db.refresh(db_product_image)
    return db_product_image

@router.delete("/{product_image_id}")
async def delete_product_image(product_image_id: int, db: AsyncSession = Depends(get_db)):
    query = select(ProductImage).where(ProductImage.id == product_image_id)
    result = await db.execute(query)
    db_product_image = result.scalar_one_or_none()
    
    if not db_product_image:
        raise HTTPException(status_code=404, detail="Изображение товара не найдено")
    
    await db.delete(db_product_image)
    await db.commit()
    
    return {"message": "Изображение товара удалено"}