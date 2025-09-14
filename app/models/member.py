from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class MemberStatusEnum(str, enum.Enum):
    pending = "pending"
    active = "active"
    inactive = "inactive"
    canceled = "canceled"


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    position = Column(String)
    biography = Column(String)
    document = Column(String)  # CPF
    photo_url = Column(String)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    status = Column(ENUM(MemberStatusEnum))
    expired_at = Column(Date)  # Data de expiração do acesso - apenas para o perfil standalone_profile
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    address = relationship("Address", back_populates="members")
    profile = relationship("Profile", back_populates="members")
    contact_channels = relationship("ContactChannel", back_populates="member")
    additional_info = relationship("AdditionalInfo", back_populates="member", uselist=False)
    performance_events = relationship("PerformanceEvent", back_populates="member")
    member_companies = relationship("MemberCompany", back_populates="member")
