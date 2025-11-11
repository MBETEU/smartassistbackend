from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Text, func
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # plus unique=True
    user_id = Column(Integer, ForeignKey("users.id"))

    notes = relationship("Note", back_populates="category", cascade="all, delete-orphan")
    user = relationship("User", back_populates="categories")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    summary = Column(Text, nullable=True)
    tags = Column(String(255), nullable=True) 

    user = relationship("User", back_populates="notes")
    category = relationship("Category", back_populates="notes")
