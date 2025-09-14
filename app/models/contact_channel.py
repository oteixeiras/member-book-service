from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class ContactChannelTypeEnum(str, enum.Enum):
    whatsapp = "whatsapp"
    email = "email"
    instagram = "instagram"
    linkedin = "linkedin"
    phone = "phone"
    others = "others"


class ContactChannel(Base):
    __tablename__ = "contact_channels"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(ENUM(ContactChannelTypeEnum), nullable=False)
    content = Column(String)
    member_id = Column(Integer, ForeignKey("members.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    member = relationship("Member", back_populates="contact_channels")
