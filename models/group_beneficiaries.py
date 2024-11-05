from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.basemodel import BaseModel, Base

class GroupBeneficiary(BaseModel, Base):
    __tablename__ = 'group_beneficiaries'
    group_id = Column(String(60), ForeignKey("Alumni_groups.id", ondelete="CASCADE"))
    beneficiary_id = Column(String(60), ForeignKey("Beneficiaries.id", ondelete="CASCADE"))
    
    
    member_id = Column(String(60), ForeignKey('group_members.id'))
    group_members = relationship("GroupMember", back_populates="beneficiaries")