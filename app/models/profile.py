from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class ProfileTypeEnum(str, enum.Enum):
    eternity = "eternity"
    infinity = "infinity"
    admin = "admin"
    standalone_profile = "standalone_profile"


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(ENUM(ProfileTypeEnum), nullable=False)
    description = Column(String)
    rule_activation = Column(JSON)
    plan_price = Column(Integer)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    members = relationship("Member", back_populates="profile")
