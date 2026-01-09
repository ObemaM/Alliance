from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ProductAttribute(Base):
    __tablename__ = "product_attributes"

    # Составной первичный ключ
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), primary_key=True)
    attribute_id: Mapped[int] = mapped_column(ForeignKey("attributes.id"), primary_key=True)
    value_text: Mapped[str | None] = mapped_column(String, nullable=True)

    product: Mapped["Product"] = relationship("Product", back_populates="product_attributes")
    attribute: Mapped["Attribute"] = relationship("Attribute", back_populates="product_attributes")

    def __repr__(self):
        return f"ProductAttribute(product_id={self.product_id}, attribute_id={self.attribute_id})"