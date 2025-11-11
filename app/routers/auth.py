from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.db.database import get_db
from app.db import models
from app.schemas.user_schemas import UserCreate, Token, UserOut
from app.services.user_service import create_user, authenticate_user
from app.core.config import settings  # ✅ correspond à ton config.py

router = APIRouter(prefix="/api/auth", tags=["Auth"])

# OAuth2 schema pour FastAPI (token récupéré dans l'en-tête Authorization)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Récupération des valeurs de configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Créer un nouvel utilisateur"""
    return create_user(db, user)


@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    """Authentifie un utilisateur et renvoie un JWT"""
    db_user = authenticate_user(db, user.email, user.password)
    # 👇 plus d'appel à db_user.email avant qu'on ait validé que c'est bien un User
    if not db_user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": db_user.email, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Récupère l'utilisateur courant à partir du JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
