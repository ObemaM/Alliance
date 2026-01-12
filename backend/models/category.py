from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from typing import List

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    # Связь с самой собой (рекурсия)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    
    # id - это удаленная сторона (на которю ссылаемся)
    parent: Mapped["Category"] = relationship("Category", remote_side=[id])
    # Это надо для рекурсии - для нахождения всех записей в дереве
    children: Mapped[List["Category"]] = relationship("Category", back_populates="parent")

    def __str__(self) -> str:
        return self.name