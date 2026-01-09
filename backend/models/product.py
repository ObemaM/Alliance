from datetime import datetime

from sqlalchemy import BigInteger, String, Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)
    pack_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    weight: Mapped[str | None] = mapped_column(String(100), nullable=True)

    color_id: Mapped[int | None] = mapped_column(ForeignKey("colors.id"), nullable=True)
    material_id: Mapped[int | None] = mapped_column(ForeignKey("materials.id"), nullable=True)
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"), nullable=True)

    # Связи с другими таблицами
    category: Mapped["Category"] = relationship("Category", lazy="select")
    color: Mapped["Color"] = relationship("Color", lazy="select")
    material: Mapped["Material"] = relationship("Material", lazy="select")
    country: Mapped["Country"] = relationship("Country", lazy="select")
    product_attributes: Mapped[list["ProductAttribute"]] = relationship(
        "ProductAttribute", back_populates="product"
    )
    product_images: Mapped[list["ProductImage"]] = relationship(
        "ProductImage", back_populates="product"
    )
    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="product"
    )

    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"Product(id={self.id}, name={self.name}, price={self.price}, "
            f"quantity={self.quantity})"
        )
