from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Color(Base):
    __tablename__ = "colors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str | None] = mapped_column(String(10), nullable=True)

    def __repr__(self):
        return f"Color(id={self.id}, name={self.name}, code={self.code})"