from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Category, Note
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"]
)

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    total_categories = db.query(Category).filter(
        Category.user_id == current_user.id
    ).count()

    total_notes = db.query(Note).filter(
        Note.user_id == current_user.id
    ).count()

    return {
        "total_categories": total_categories,
        "total_notes": total_notes
    }

@router.get("/notes-by-category")
def get_notes_by_category(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Récupérer toutes les catégories de l'utilisateur
    categories = db.query(Category).filter(
        Category.user_id == current_user.id
    ).all()

    data = []

    for cat in categories:
        count_notes = db.query(Note).filter(
            Note.category_id == cat.id,
            Note.user_id == current_user.id
        ).count()

        data.append({
            "category": cat.name,
            "count": count_notes
        })

    return data

