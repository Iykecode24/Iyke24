import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    creator = "creator"
    editor = "editor"
    viewer = "viewer"

class User(Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    display_name: Mapped[str] = mapped_column(String)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.creator)
    mfa_secret: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="user")
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="user")
    social_accounts: Mapped[List["SocialAccount"]] = relationship("SocialAccount", back_populates="user")
    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="user")
