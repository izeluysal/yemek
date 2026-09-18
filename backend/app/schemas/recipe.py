from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# --- Etiket (Tag) Şemaları ---

class TagBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Etiket adı")


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Tarif (Recipe) Şemaları ---

class RecipeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, description="Yemek başlığı")
    slug: str = Field(..., min_length=3, max_length=255, description="URL dostu başlık")
    description: Optional[str] = Field(default=None, description="Kısa özet")
    ingredients: List[str] = Field(default_factory=list, description="Malzeme listesi")
    instructions: str = Field(..., min_length=10, description="Adım adım yapılış")
    prep_time: Optional[int] = Field(default=None, ge=0, description="Hazırlık süresi (dakika)")
    cook_time: Optional[int] = Field(default=None, ge=0, description="Pişirme süresi (dakika)")


class RecipeCreate(RecipeBase):
    tags: List[str] = Field(default_factory=list, description="Tarife atanacak etiket isimleri")


class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=255)
    slug: Optional[str] = Field(default=None, min_length=3, max_length=255)
    description: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[str] = Field(default=None, min_length=10)
    image_url: Optional[str] = None
    prep_time: Optional[int] = Field(default=None, ge=0)
    cook_time: Optional[int] = Field(default=None, ge=0)
    tags: Optional[List[str]] = None


class RecipeResponse(RecipeBase):
    id: int
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = []

    model_config = ConfigDict(from_attributes=True)