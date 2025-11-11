from sqlalchemy.orm import Session
from app.db import models
from app.utils.hashing import hash_password, verify_password
from app.core.security import create_access_token
from app.schemas.user_schemas import UserCreate
from fastapi import HTTPException, status

def create_user(db: Session, user: UserCreate):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà enregistré.")
    hashed_pw = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides.")
    return user  # 👈 retourne l'objet User


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
