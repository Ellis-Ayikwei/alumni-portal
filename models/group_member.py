from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base

class Status(enum.Enum):
    PENDING = "PENDING"
    DISAPPROVED = "DISAPPROVED"
    APPROVED = "APPROVED"


class GroupMember(BaseModel, Base):
    __tablename__ = 'group_members'


    user_id = Column(String(60), ForeignKey('users.id'), nullable=False, unique=True)
    added_by = Column(String(60), ForeignKey('users.id'),  nullable=True)
    group_id = Column(String(60), ForeignKey('alumni_groups.id'), nullable=False)
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    is_approved = Column(Boolean, default=False)
    beneficiaries = relationship("Beneficiary", back_populates="group_members")
    user_info = relationship("User", back_populates="group_memberships", foreign_keys=[user_id])
    added_by_user = relationship("User", foreign_keys=[added_by])
    
    
    def to_dict(self):
        dict_data = super().to_dict()
        
        if isinstance(self.status, Status):
            dict_data["status"] = self.status.name
        else:
            dict_data["status"] = self.status

        return dict_data
    
    def set_isApproved(self):
        """
        Set the is_approved attribute of the group member to True
        """
        self.is_validated = True
        