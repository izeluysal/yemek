from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.recipe import Recipe, Tag
from app.schemas.recipe import RecipeCreate, RecipeResponse
from app.services.image import process_and_save_image

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("", response_model=List[RecipeResponse])
def get_recipes(
    q: Optional[str] = Query(None, description="Başlık veya açıklamada arama"),
    tag: Optional[str] = Query(None, description="Etiket adına göre filtreleme"),
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)

    if q:
        search_pattern = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Recipe.title.ilike(search_pattern),
                Recipe.description.ilike(search_pattern)
            )
        )

    if tag:
        query = query.join(Recipe.tags).filter(Tag.name == tag.strip().lower())

    return query.order_by(Recipe.created_at.desc()).all()


@router.get("/{slug}", response_model=RecipeResponse)
def get_recipe_by_slug(slug: str, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.slug == slug).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarif bulunamadı."
        )
    return recipe


@router.post("", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(recipe_in: RecipeCreate, db: Session = Depends(get_db)):
    existing_recipe = db.query(Recipe).filter(Recipe.slug == recipe_in.slug).first()
    if existing_recipe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu URL uzantısı (slug) zaten kullanımda."
        )

    recipe_data = recipe_in.model_dump(exclude={"tags"})
    recipe = Recipe(**recipe_data)

    if recipe_in.tags:
        for tag_name in recipe_in.tags:
            cleaned_tag = tag_name.strip().lower()
            if not cleaned_tag:
                continue
            db_tag = db.query(Tag).filter(Tag.name == cleaned_tag).first()
            if not db_tag:
                db_tag = Tag(name=cleaned_tag)
                db.add(db_tag)
            recipe.tags.append(db_tag)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.post("/{recipe_id}/image", response_model=RecipeResponse)
async def upload_recipe_image(
    recipe_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarif bulunamadı."
        )

    image_path = await process_and_save_image(file)
    recipe.image_url = image_path
    db.commit()
    db.refresh(recipe)
    return recipe