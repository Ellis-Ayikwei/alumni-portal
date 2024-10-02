from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.basemodel import BaseModel, Base

class Beneficiary(BaseModel, Base):
    __tablename__ = 'beneficiaries'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date)
    relationship_type = Column(String(50))  # Renamed to avoid conflict
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    member_id = Column(Integer, ForeignKey('members.id'))
    member = relationship("Member", back_populates="beneficiaries")  # SQLAlchemy relationship
