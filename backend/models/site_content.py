from sqlalchemy import BigInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class SiteContent(Base):
    __tablename__ = "site_content"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # уникальный ключ
    value: Mapped[str] = mapped_column(Text, nullable=False)  # значение (может быть длинным)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)  # описание для админа

    def __repr__(self):
        return f"SiteContent(key={self.key}, value={self.value[:50]}...)"
