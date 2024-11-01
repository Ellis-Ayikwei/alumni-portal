from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base

class Status(enum.Enum):
    PENDING = "PENDING"
    VALIDATED = "VALIDATED"


class GroupMember(BaseModel, Base):
    __tablename__ = 'group_members'


    
    added_by = Column(String(60), ForeignKey('users.id'))
    group_id = Column(String(60), ForeignKey('alumni_groups.id'))
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    is_validated = Column(Boolean, default=False)
    beneficiaries = relationship("Beneficiary", back_populates="group_members")
    
    
    
    # def to_dict(self):
    #     dict_data = super().to_dict()
        
    #     if isinstance(self.status, Status):
    #         dict_data["status"] = self.status.name
    #     else:
    #         dict_data["status"] = self.status

    #     return dict_data
        