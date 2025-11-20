from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.models import Category
from app.schemas.category_schemas import CategoryCreate, CategoryOut
from app.db.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(tags=["categories"])

@router.post("/", response_model=CategoryOut)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
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

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Catégorie introuvable"
        )

    db.delete(category)
    db.commit()

    return {"message": "Catégorie supprimée avec succès"}

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Catégorie introuvable"
        )

    # Vérifier si un autre nom identique existe déjà pour ce user
    duplicate = db.query(Category).filter(
        Category.name == data.name,
        Category.user_id == current_user.id,
        Category.id != category_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Une catégorie avec ce nom existe déjà"
        )

    category.name = data.name
    db.commit()
    db.refresh(category)

    return category
