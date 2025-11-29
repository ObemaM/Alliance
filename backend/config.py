from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Alliance"
    debug: bool = True
    cors_origins: list = ["*"] # Потом сменить, ибо сейчас разрешены все
    #cors_origins = ["https://alliance-app.com","https://www.alliance-app.com","http://localhost:3000"]

    # Настройки базы данных
    DB_USER: str = "postgres"
    DB_PASS: str = "alliance"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5435
    DB_NAME: str = "Alliance"

    # @property нужен просто для того, чтобы вызывать метод без скобок (как свойство), это просто для удобства
    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Указывает на файл .env
    model_config = SettingsConfigDict(env_file="../.env")

    IMAGES: str = "uploads/images"

    # Максимальный размер файла (5 МБ), чтобы сервер не положили
    MAX_SIZE: int = 5 

    # Разрешенные форматы
    ALLOWED_EXTENSIONS: list = ["jpg", "jpeg", "png", "webp"]

settings = Settings()