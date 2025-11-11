from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import auth, notes, categories


app = FastAPI(title="SmartAssist Backend")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(categories.router)

