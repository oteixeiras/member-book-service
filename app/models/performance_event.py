from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class PerformanceEventTypeEnum(str, enum.Enum):
    referral = "referral"
    transaction = "transaction"


class PerformanceEvent(Base):
    __tablename__ = "performance_events"

    id = Column(Integer, primary_key=True, index=True)
    performance_id = Column(Integer, ForeignKey("performance.id"))
    event_id = Column(Integer, autoincrement=True)
    type = Column(ENUM(PerformanceEventTypeEnum), nullable=False)
    value = Column(Integer)
    member_id = Column(Integer, ForeignKey("members.id"))  # Opcional caso seja uma transação
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    performance = relationship("Performance", back_populates="performance_events")
    member = relationship("Member", back_populates="performance_events")
