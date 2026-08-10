import uuid
from sqlalchemy import ForeignKey, String, Boolean, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum

class ImageType(str, enum.Enum):
    front = "front"
    side = "side"
    full_body = "full_body"
    additional = "additional"

class CharacterReference(Base):
    __tablename__ = "character_references"
    
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id"))
    image_url: Mapped[str] = mapped_column(String)
    image_type: Mapped[ImageType] = mapped_column(Enum(ImageType))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    width: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    height: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    character: Mapped["Character"] = relationship("Character", back_populates="references")
