from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from schemas.order_item import OrderItemResponse, OrderItemCreate, OrderItemUpdate
from models.order_item import OrderItem

router = APIRouter(prefix="/order_items", tags=["Order Items"])

@router.get("/", response_model=list[OrderItemResponse])
async def get_all_order_items(db: AsyncSession = Depends(get_db)):
    query = select(OrderItem)
    result = await db.execute(query)
    items = result.scalars().all()
    return items

@router.get("/order/{order_id}", response_model=list[OrderItemResponse])
async def get_items_by_order(order_id: int, db: AsyncSession = Depends(get_db)):
    query = select(OrderItem).where(OrderItem.order_id == order_id)
    result = await db.execute(query)
    items = result.scalars().all()
    return items

@router.post("/", response_model=OrderItemResponse)
async def create_order_item(item: OrderItemCreate, db: AsyncSession = Depends(get_db)):
    new_item = OrderItem(
        product_id=item.product_id,
        order_id=item.order_id,
        quantity=item.quantity,
        price_at_purchase=item.price_at_purchase
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.patch("/{product_id}/{order_id}", response_model=OrderItemResponse)
async def update_order_item(
    product_id: int,
    order_id: int,
    item: OrderItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(OrderItem).where(
        OrderItem.product_id == product_id,
        OrderItem.order_id == order_id
    )
    result = await db.execute(query)
    db_item = result.scalar_one_or_none()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Позиция заказа не найдена")
    
    if item.product_id is not None:
        db_item.product_id = item.product_id
    if item.order_id is not None:
        db_item.order_id = item.order_id
    if item.quantity is not None:
        db_item.quantity = item.quantity
    if item.price_at_purchase is not None:
        db_item.price_at_purchase = item.price_at_purchase
    
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.delete("/{product_id}/{order_id}")
async def delete_order_item(
    product_id: int,
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    query = select(OrderItem).where(
        OrderItem.product_id == product_id,
        OrderItem.order_id == order_id
    )
    result = await db.execute(query)
    db_item = result.scalar_one_or_none()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Позиция заказа не найдена")
    
    await db.delete(db_item)
    await db.commit()
    
    return {"message": "Позиция заказа удалена"}
