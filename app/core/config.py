from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "Dubflow Backend"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/dubflow")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
    LIBRETRANSLATE_URL: str = os.getenv("LIBRETRANSLATE_URL", "https://libretranslate.de/translate")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "uploads/translated")

    class Config:
        env_file = ".env"


settings = Settings()