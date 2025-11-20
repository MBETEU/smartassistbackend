from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.routers import auth, notes, categories

app = FastAPI(title="SmartAssist Backend")

# --- CORS CONFIGURATION ---
origins = [
    "http://localhost:3000",     # React Dev Server
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # IMPORTANT : pas de "*"
    allow_credentials=True,
    allow_methods=["*"],          # Autorise GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],
)

# --- DATABASE INIT ---
Base.metadata.create_all(bind=engine)

# --- ROUTERS ---
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])

