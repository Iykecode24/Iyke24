import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import String, Boolean, Enum, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class DocumentType(str, enum.Enum):
    privacy_policy = "privacy_policy"
    terms_of_service = "terms_of_service"

class LegalDocument(Base):
    __tablename__ = "legal_documents"
    
    document_type: Mapped[DocumentType] = mapped_column(Enum(DocumentType), index=True)
    version: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    consents: Mapped[List["UserConsent"]] = relationship("UserConsent", back_populates="document")

class UserConsent(Base):
    __tablename__ = "user_consents"
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    document_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("legal_documents.id"), index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    agreed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    
    document: Mapped["LegalDocument"] = relationship("LegalDocument", back_populates="consents")
