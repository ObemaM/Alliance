from sqlalchemy import BigInteger, Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    # Составной первичный ключ
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_purchase: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)

    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
    order: Mapped["Order"] = relationship("Order", back_populates="order_items")

    def __repr__(self):
        return f"OrderItem(product_id={self.product_id}, order_id={self.order_id}, quantity={self.quantity})"