from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import countries_router
from routes import colors_router
from routes import categories_router
from routes import materials_router
from routes import products_router
from routes import site_content_router

from fastapi.staticfiles import StaticFiles

# ./venv/Scripts/activate

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
app.include_router(categories_router)
app.include_router(materials_router)
app.include_router(products_router)
app.include_router(site_content_router)

# Главная страница API
@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name} API"}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Подключаем админку
from admin import admin

