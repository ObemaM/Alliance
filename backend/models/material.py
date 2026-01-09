from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Material(Base):
    __tablename__ = "materials"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"Material(id={self.id}, name={self.name})"