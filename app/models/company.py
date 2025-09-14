from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    market_segmentation_id = Column(Integer, ForeignKey("market_segmentation.id"))
    address_id = Column(Integer, ForeignKey("addresses.id"))
    document = Column(String)  # CNPJ
    founded_year = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    market_segmentation = relationship("MarketSegmentation", back_populates="companies")
    address = relationship("Address", back_populates="companies")
    performances = relationship("Performance", back_populates="company")
    member_companies = relationship("MemberCompany", back_populates="company")
