import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine
from app.models.recipe import Base
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Uygulama ayağa kalkarken: uploads dizinini ve tabloları hazırla
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# Güvenlik & CORS Politikası
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Görsellerin sunulması için uploads dizinini dışa aç
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# API rotalarını bağla
app.include_router(api_router, prefix="/api")


@app.get("/health", tags=["system"])
def health_check():
    """Konteyner ve sunucu sağlık kontrolü."""
    return {"status": "ok", "app": settings.PROJECT_NAME}