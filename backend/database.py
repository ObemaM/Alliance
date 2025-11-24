from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import settings

# echo - печатает запросы в консоль для обработки ошибок, при разработке = true, потом false
# expire_on_commit=False - чтобы не было проблем с сессиями
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Фабрика сессий для создания сессий для разных действий
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Базовый класс для всех таблиц
class Base(DeclarativeBase):
    pass

# Пришел запрос от пользователя -> СОЗДАЕМ НОВУЮ сессию
async def get_db():
    # Отдаем сессию функции, которая обрабатывает запрос
    async with SessionLocal() as session:
        # yield останавливает функцию, пока роутер не закончит выполнение 
        yield session
    # Закрываем сессию, благодаря async with это происходит автоматически
