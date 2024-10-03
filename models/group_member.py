from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base

# class Status(enum.Enum):
#     PENDING = "PENDING"
#     VALIDATED = "VALIDATED"


class GroupMember(BaseModel, Base):
    __tablename__ = 'group_members'


    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_names = Column(String(100))
    gender = Column(String(10))
    cellphone = Column(String(20))
    date_of_birth = Column(Date)
    is_validated = Column(Boolean, default=False)
    added_by = Column(String(60), ForeignKey('users.id'))
    email = Column(String(60), nullable=False)
    Alumni_group_id = Column(String(60), ForeignKey('alumni_groups.id'))
    group = relationship("AlumniGroup", back_populates="group_members")
    beneficiaries = relationship("Beneficiary", back_populates="group_members")
    contract_members = relationship("ContractMember", back_populates="group_members")
    
    
    
    # def to_dict(self):
    #     dict_data = super().to_dict()
        
    #     if isinstance(self.status, Status):
    #         dict_data["status"] = self.status.name
    #     else:
    #         dict_data["status"] = self.status

    #     return dict_data
        