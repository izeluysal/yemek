import os
import uuid
from io import BytesIO
from typing import Tuple
from PIL import Image, ImageOps
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

# İzin verilen MIME tipleri ve uzantılar
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_DIMENSION = 2048  # Web vitrini için dengeli maksimum piksel boyutu (genişlik/yükseklik)


def validate_image_file(file: UploadFile) -> None:
    """Dosya boyutu ve MIME tipi temel doğrulaması."""
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Geçersiz dosya formatı. Yalnızca JPEG, PNG ve WebP kabul edilir."
        )


async def process_and_save_image(file: UploadFile) -> str:
    """
    Yüklenen görseli güvenli bir şekilde işler:
    - EXIF verilerini temizler.
    - Gerekirse maksimum boyutlara küçültür.
    - WebP formatında sıkıştırıp UUID adıyla kaydeder.
    - Dönen değer: /uploads/<uuid>.webp göreli yolu.
    """
    validate_image_file(file)

    # Dosya içeriğini belleğe oku
    content = await file.read()
    if len(content) > settings.MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Dosya boyutu en fazla {settings.MAX_IMAGE_SIZE_BYTES // (1024 * 1024)} MB olabilir."
        )

    try:
        image = Image.open(BytesIO(content))
        # Yönelim EXIF verisine göre düzeltilir, ardından EXIF atılır
        image = ImageOps.exif_transpose(image)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Geçersiz veya bozuk görsel dosyası."
        )

    # Saydamlık kontrolü (RGBA ise koru, değilse RGB'ye çevir)
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")

    # Çözünürlük optimizasyonu (Maksimum sınır)
    image.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.Resampling.LANCZOS)

    # Dosya adını UUID ile üret
    filename = f"{uuid.uuid4().hex}.webp"
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    destination_path = os.path.join(settings.UPLOAD_DIR, filename)

    # WebP formatında optimize ederek diske yaz
    image.save(destination_path, format="WEBP", quality=82, optimize=True)

    # Tarayıcıdan erişilecek statik yol formatı
    return f"/uploads/{filename}"