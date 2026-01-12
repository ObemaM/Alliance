from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

# Таблица countries
class Country(Base):
    __tablename__ = "countries"
    
    # id - автоинкремент, первичный ключ
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # name - строка до 100 символов (varchar(100))
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return f"Country(id={self.id}, name={self.name})"
