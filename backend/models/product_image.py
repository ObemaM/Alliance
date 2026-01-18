from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    url: Mapped[str | None] = mapped_column(String, nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="product_images")

    def __repr__(self):
        return f"ProductImage(product_id={self.product_id}, url={self.url})"