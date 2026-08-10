from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime, Float, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class AIModel(Base):
    __tablename__ = "ai_models"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, unique=True)
    provider = Column(String, nullable=False) # e.g., 'openai'
    model_type = Column(String, nullable=False) # 'reasoning', 'metadata', 'memory', 'vision', etc.
    version = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AIAgent(Base):
    __tablename__ = "ai_agents"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, unique=True) # e.g., 'Creative Director'
    role = Column(String, nullable=False)
    system_prompt = Column(Text, nullable=False)
    model_id = Column(String, ForeignKey("ai_models.id"), nullable=False)
    max_loops = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)

    model = relationship("AIModel")

class AIUsage(Base):
    __tablename__ = "ai_usage"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=True)
    agent_id = Column(String, ForeignKey("ai_agents.id"), nullable=True)
    model_id = Column(String, ForeignKey("ai_models.id"), nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    model = relationship("AIModel")
    agent = relationship("AIAgent")
    project = relationship("Project")

class ProjectMemory(Base):
    __tablename__ = "project_memories"

    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    key = Column(String, nullable=False)
    value = Column(JSON, nullable=False)
    embedding = Column(JSON, nullable=True) # Store vector representation for search if needed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project")
