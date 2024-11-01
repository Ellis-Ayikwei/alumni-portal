from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.basemodel import BaseModel, Base

class Beneficiary(BaseModel, Base):
    __tablename__ = 'beneficiaries'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date)
    relationship_type = Column(String(50))

    member_id = Column(String(60), ForeignKey('group_members.id'))
    group_members = relationship("GroupMember", back_populates="beneficiaries")
