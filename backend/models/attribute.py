from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Attribute(Base):
    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    product_attributes: Mapped[list["ProductAttribute"]] = relationship(
        "ProductAttribute", back_populates="attribute"
    )

    def __repr__(self):
        return self.name
