from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base



class ContractMember(BaseModel, Base):
    __tablename__ = 'contract_members'

    
    is_amended = Column(Boolean, default=False)
    
    contract_id = Column(String(60), ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="contract_members")
    group_member_id = Column(String(60), ForeignKey('group_members.id'))
    group_members = relationship("GroupMember", back_populates="contract_members")