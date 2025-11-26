from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import countries_router
from routes import colors_router

# Запуск - uvicorn main:app --reload
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

# Настройка CORS (разрешаем запросы с фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(countries_router)
app.include_router(colors_router)

# Главная страница API
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name} API"}

