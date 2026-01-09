from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from schemas.order import OrderResponse, OrderCreate, OrderUpdate
from models.order import Order

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=list[OrderResponse])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    query = select(Order)
    result = await db.execute(query)
    orders = result.scalars().all()
    return orders

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    new_order = Order(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_email=order.customer_email,
        delivery_address=order.delivery_address,
        notes=order.notes,
        total_amount=order.total_amount,
        status=order.status
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order: OrderUpdate,
    db: AsyncSession = Depends(get_db)
):
    query = select(Order).where(Order.id == order_id)
    result = await db.execute(query)
    db_order = result.scalar_one_or_none()
    
    if not db_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    if order.customer_name is not None:
        db_order.customer_name = order.customer_name
    if order.customer_phone is not None:
        db_order.customer_phone = order.customer_phone
    if order.customer_email is not None:
        db_order.customer_email = order.customer_email
    if order.delivery_address is not None:
        db_order.delivery_address = order.delivery_address
    if order.notes is not None:
        db_order.notes = order.notes
    if order.total_amount is not None:
        db_order.total_amount = order.total_amount
    if order.status is not None:
        db_order.status = order.status
    
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.delete("/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Order).where(Order.id == order_id)
    result = await db.execute(query)
    db_order = result.scalar_one_or_none()
    
    if not db_order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    
    await db.delete(db_order)
    await db.commit()
    
    return {"message": "Заказ удалён"}
