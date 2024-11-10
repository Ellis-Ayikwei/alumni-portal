from http.client import LOCKED
from click import group
from colorama import Fore
from sqlalchemy import Column, Index, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models import group_member
from models.basemodel import BaseModel, Base
from models.contract import Contract
from models.group_member import GroupMember

class Status(enum.Enum):
    ACTIVATED = "ACTIVATED"
    DEACTIVATED = "DEACTIVATED"
    LOCKED = "LOCKED"
    
class AlumniGroup(BaseModel, Base):
    __tablename__ = 'alumni_groups'

    id = Column(String(60), primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    school = Column(String(100), nullable=False)
    status = Column(Enum(Status), default=Status.ACTIVATED)
    package_id = Column(String(60), ForeignKey('insurance_packages.id', ondelete="SET NULL"), nullable=True)
    description = Column(String(255), nullable=True)
    current_contract_id = Column(String(60), ForeignKey('contracts.id', ondelete="SET NULL"), nullable=True)
    
    president_user_id = Column(String(60), ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    
    president = relationship("User", back_populates="groups_as_president", foreign_keys=[president_user_id])
    payments = relationship("Payment", back_populates="group")
    members = relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    
    # Explicit foreign key specification for contracts
    contracts = relationship("Contract", back_populates="group", foreign_keys=[Contract.group_id])
    current_contract = relationship("Contract", foreign_keys=[current_contract_id])
    
    insurance_package = relationship("InsurancePackage", back_populates="groups")

    __table_args__ = (
        Index('ix_alumni_groups_name', 'name'),
        Index('ix_alumni_groups_school', 'school'),
        Index('ix_alumni_groups_status', 'status'),
    )
    
    def to_dict(self, save_fs=None):
        dict_data = super().to_dict()
        
        if isinstance(self.status, Status):
            dict_data["status"] = self.status.name
        else:
            dict_data["status"] = self.status
        
        # Contracts list simplified, including only basic info
        dict_data["contracts"] = [{"id": contract.id, "name": contract.name} for contract in self.contracts]
        dict_data["current_contract"] = {"id": self.current_contract.id, "name": self.current_contract.name} if self.current_contract else None

        return dict_data
