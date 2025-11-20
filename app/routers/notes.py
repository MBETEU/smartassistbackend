from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db import models
from app.schemas.note_schemas import NoteCreate, NoteOut, NoteUpdate
from app.dependencies import get_current_user
from app.services.ai_service import generate_summary, generate_tags

router = APIRouter(tags=["Notes"])

def enrich_note_with_ai(note_id: int, db: Session):
    """
    Met à jour la note avec un résumé et des tags générés par l'IA.
    Les tags sont stockés comme liste dans la colonne 'tags'.
    """
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        return
    try:
        note.summary = generate_summary(note.content)
        note.tags = generate_tags(note.content)  # liste de tags
        db.commit()
    except Exception as e:
        print(f"⚠️ Erreur IA : {e}")

@router.post("/", response_model=NoteOut)
def create_note(
    note: NoteCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Créer une note et lancer le traitement IA en arrière-plan."""
    db_category = None
    if note.category_id:
        db_category = db.query(models.Category).filter(
            models.Category.id == note.category_id,
            models.Category.user_id == current_user.id
        ).first()
        if not db_category:
            raise HTTPException(status_code=404, detail="Catégorie non trouvée")

    db_note = models.Note(
        title=note.title,
        content=note.content,
        category_id=note.category_id,
        user_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    # Lancer l'enrichissement IA en arrière-plan
    background_tasks.add_task(enrich_note_with_ai, db_note.id, db)

    return db_note

@router.get("/", response_model=List[NoteOut])
def list_notes(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Lister les notes de l'utilisateur, filtrables par catégorie ou recherche."""
    query = db.query(models.Note).filter(models.Note.user_id == current_user.id)
    if category_id:
        query = query.filter(models.Note.category_id == category_id)
    if search:
        query = query.filter(models.Note.title.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/{note_id}", response_model=NoteOut)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Récupérer une note par son ID."""
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return note

@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    note_update: NoteUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Mettre à jour une note et relancer l'enrichissement IA si contenu modifié."""
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note non trouvée")

    updated_fields = note_update.dict(exclude_unset=True)
    for field, value in updated_fields.items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)

    # Lancer l'enrichissement IA si le contenu a changé
    if "content" in updated_fields:
        background_tasks.add_task(enrich_note_with_ai, note.id, db)

    return note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Supprimer une note."""
    note = db.query(models.Note).filter(
        models.Note.id == note_id,
        models.Note.user_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    db.delete(note)
    db.commit()
    return {"detail": "Note supprimée avec succès"}
