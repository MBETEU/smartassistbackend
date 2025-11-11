from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.models import Category
from app.schemas.category_schemas import CategoryCreate, CategoryOut
from app.db.database import get_db
from app.routers.auth import get_current_user  # dépend de ton système auth

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"]
)

@router.post("/", response_model=CategoryOut)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Vérifier si la catégorie existe déjà pour l'utilisateur
    existing_category = db.query(Category).filter(
        Category.name == category.name,
        Category.user_id == current_user.id
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Cette catégorie existe déjà"
        )
    
    db_category = Category(
        name=category.name,
        user_id=current_user.id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/", response_model=List[CategoryOut])
def get_categories(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    categories = db.query(Category).filter(
        Category.user_id == current_user.id
    ).all()
    return categories
