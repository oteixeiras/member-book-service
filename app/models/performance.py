from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    count_closed_deals = Column(Integer)  # Quantidade de negócios fechados
    value_closed_deals = Column(Integer)  # Valor dos negócios fechados
    referrals_received = Column(Integer)  # Quantidade de indicações recebidas
    total_value_per_referral = Column(Integer)  # Valor total por indicações
    referrals_given = Column(Integer)  # Quantidade de indicações fornecidas
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company = relationship("Company", back_populates="performances")
    performance_events = relationship("PerformanceEvent", back_populates="performance")
