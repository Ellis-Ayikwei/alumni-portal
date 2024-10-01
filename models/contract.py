from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base


class Contract(BaseModel, Base):
    __tablename__ = 'contracts'

    
    contract_id = Column(String(50), unique=True, nullable=False)
    

    group_id = Column(Integer, ForeignKey('alumni_groups.id'))
    group = relationship("AlumniGroup", back_populates="contracts")
    contract_members = relationship("ContractMember", back_populates="contract")