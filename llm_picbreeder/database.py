"""
Database interface for LLM-Picbreeder
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from .config import settings

Base = declarative_base()

class DBPrompt(Base):
    __tablename__ = "prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    template_vars = Column(JSON)
    metadata_json = Column(JSON)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("prompts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    complexity_score = Column(Float, default=0.0)
    
    # Relationships
    children = relationship("DBPrompt", back_populates="parent")
    parent = relationship("DBPrompt", back_populates="children", remote_side=[id])
    evaluations = relationship("DBEvaluation", back_populates="prompt")
    creator = relationship("DBUser", back_populates="prompts")

class DBEvaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    output_content = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    prompt = relationship("DBPrompt", back_populates="evaluations")
    user = relationship("DBUser", back_populates="evaluations")

class DBUser(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    prompts = relationship("DBPrompt", back_populates="creator")
    evaluations = relationship("DBEvaluation", back_populates="user")

class DBLineage(Base):
    __tablename__ = "lineages"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)
    ancestor_ids = Column(JSON)
    generation = Column(Integer, default=0)
    branch_point = Column(Integer, nullable=True)

# Create database engine and session
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()