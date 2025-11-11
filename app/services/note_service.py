from sqlalchemy.orm import Session
from app.db import models
from app.schemas.note_schemas import NoteCreate, CategoryCreate
from fastapi import HTTPException, status

# Notes
def create_note(db: Session, note: NoteCreate, user_id: int):
    db_note = models.Note(**note.dict(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(db: Session, user_id: int, skip: int = 0, limit: int = 10, category_id: int = None, search: str = None):
    query = db.query(models.Note).filter(models.Note.user_id == user_id)
    if category_id:
        query = query.filter(models.Note.category_id == category_id)
    if search:
        query = query.filter(models.Note.title.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def get_note(db: Session, note_id: int, user_id: int):
    note = db.query(models.Note).filter(models.Note.id == note_id, models.Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return note

def update_note(db: Session, note_id: int, user_id: int, note_data: NoteCreate):
    note = get_note(db, note_id, user_id)
    for key, value in note_data.dict(exclude_unset=True).items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note_id: int, user_id: int):
    note = get_note(db, note_id, user_id)
    db.delete(note)
    db.commit()
    return {"detail": "Note supprimée"}

# Categories
def create_category(db: Session, category: CategoryCreate):
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Catégorie déjà existante")
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(models.Category).all()
