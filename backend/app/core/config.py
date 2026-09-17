from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Yemek Tarifi Defteri"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Veritabanı Ayarları (PostgreSQL)
    POSTGRES_SERVER: str = Field(default="localhost", alias="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(default="recipe_user", alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="supersecretpassword", alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="recipe_db", alias="POSTGRES_DB")
    POSTGRES_PORT: int = Field(default=5432, alias="POSTGRES_PORT")

    # Güvenlik & Admin Yetkilendirme
    SECRET_KEY: str = Field(default="change-this-secret-key-in-production-min-32-chars", alias="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 gün

    # Medya ve Upload Limitleri
    MAX_IMAGE_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB
    ALLOWED_IMAGE_EXTENSIONS: set = {"jpg", "jpeg", "png", "webp"}
    UPLOAD_DIR: str = "uploads"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()