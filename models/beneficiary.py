from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base


class Beneficiary(BaseModel, Base):
    __tablename__ = 'beneficiaries'

    
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date)
    relationship = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    member_id = Column(Integer, ForeignKey('members.id'))
    member = relationship("Member", back_populates="beneficiaries")