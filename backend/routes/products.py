from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models.product import Product
from schemas.product import ProductResponse, ProductCreate, ProductUpdate


router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductResponse])
async def get_all_products(
    q: str | None = None,
    name: str | None = None,
    category: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: AsyncSession = Depends(get_db),
):

    # Можно сказать, что selectinload - это просто where product_id == текущему продукту
    query = select(Product).options(selectinload(Product.product_images))

    search = q or name

    if search:
        query = query.where(
            (Product.name.ilike(f"%{search}%") |
            Product.description.ilike(f"%{search}%"))
        )

    if category:
        query = query.where(Product.category_id == category)

    if min_price is not None:
        query = query.where(Product.price >= min_price)

    if max_price is not None:
        query = query.where(Product.price <= max_price)
    
    result = await db.execute(query)
    products = result.scalars().all()
    return products

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
        category_id=product.category_id,
        pack_quantity=product.pack_quantity,
        quantity=product.quantity,
        price=product.price,
        weight=product.weight,
        color_id=product.color_id,
        material_id=product.material_id,
        country_id=product.country_id,
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    db_product = result.scalar_one_or_none()

    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    if product.name is not None:
        db_product.name = product.name
    if product.description is not None:
        db_product.description = product.description
    if product.category_id is not None:
        db_product.category_id = product.category_id
    if product.pack_quantity is not None:
        db_product.pack_quantity = product.pack_quantity
    if product.quantity is not None:
        db_product.quantity = product.quantity
    if product.price is not None:
        db_product.price = product.price
    if product.weight is not None:
        db_product.weight = product.weight
    if product.color_id is not None:
        db_product.color_id = product.color_id
    if product.material_id is not None:
        db_product.material_id = product.material_id
    if product.country_id is not None:
        db_product.country_id = product.country_id

    await db.commit()
    await db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Product).where(Product.id == product_id)
    result = await db.execute(query)
    db_product = result.scalar_one_or_none()

    if not db_product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    await db.delete(db_product)
    await db.commit()

    return {"message": "Товар удалён"}
