from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None
    category_id: Optional[int] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

class NoteOut(NoteBase):
    id: int
    created_at: datetime
    user_id: int
    summary: Optional[str] = None  # Résumé généré par l'IA
    tags: Optional[List[str]] = []  # Tags générés par l'IA

    class Config:
        from_attributes = True  # Pydantic v2 : remplace orm_mode
