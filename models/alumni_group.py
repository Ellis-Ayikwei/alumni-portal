from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base

class Status(enum.Enum):
    ACTIVE = "ACTIVE"
    LOCKED = "LOCKED"
    
class AlumniGroup(BaseModel, Base):
    __tablename__ = 'alumni_groups'

    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    insurance_package = Column(String(100), nullable=False)
    is_locked = Column(Boolean, default=False)
    status = Column(Enum(Status), default=Status.ACTIVE, nullable=False)
    president_id = Column(String(60), ForeignKey('users.id'))
    president = relationship("User", back_populates="groups")
    group_members = relationship("GroupMember", back_populates="group")
    contracts = relationship("Contract", back_populates="group")
    