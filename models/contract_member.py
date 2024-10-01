from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base



class ContractMember(BaseModel, Base):
    __tablename__ = 'contract_members'

    
    is_amended = Column(Boolean, default=False)
    
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="contract_members")
    member_id = Column(Integer, ForeignKey('members.id'))
    member = relationship("Member", back_populates="contract_members")