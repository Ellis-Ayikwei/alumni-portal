from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base


class Member(BaseModel, Base):
    __tablename__ = 'members'

    
    individual_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_names = Column(String(100))
    gender = Column(String(10))
    cellphone = Column(String(20))
    date_of_birth = Column(Date)
    is_validated = Column(Boolean, default=False)
    

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="member_profile")
    group_id = Column(Integer, ForeignKey('alumni_groups.id'))
    group = relationship("AlumniGroup", back_populates="members")
    beneficiaries = relationship("Beneficiary", back_populates="members")
    contract_members = relationship("ContractMember", back_populates="members")