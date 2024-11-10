from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime
import enum
from models import payment
from models.basemodel import BaseModel, Base
import json

class Status(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"
    TERMINATED = "TERMINATED"

class Contract(BaseModel, Base):
    """
    Represents an insurance contract between an underwriter and an alumni group

    Attributes:
        group_id (str): The id of the alumni group
        expiry_date (datetime.date): The contract expiry date
        signed_date (datetime.datetime): The contract signing date
        status (ContractStatus): The contract status
        underwriter_id (str): The id of the underwriter
        insurance_package_id (str): The id of the insurance package
    """
    __tablename__ = 'contracts'
    name = Column(String(100), nullable=False)
    group_id = Column(String(60), ForeignKey('alumni_groups.id'))
    expiry_date = Column(Date, nullable=True)
    date_effective = Column(Date, nullable=True)
    is_signed = Column(Boolean, default=False)
    signed_date = Column(Date, nullable=True)
    status = Column(Enum(Status), default=Status.INACTIVE, nullable=False)
    underwriter_id = Column(String(60), ForeignKey('users.id'))
    insurance_package_id = Column(String(60), ForeignKey('insurance_packages.id', ondelete="SET NULL"), nullable=True)
    description = Column(String(255), nullable=True)
    policy_number = Column(String(100), nullable=True)
    payments = relationship("Payment", back_populates="contract")
    
    # Relationships
    group = relationship("AlumniGroup", back_populates="contracts", foreign_keys=[group_id])
    contract_members = relationship("ContractMember", back_populates="contract")
    underwriter = relationship("User", backref="contracts")
    amendments = relationship("Amendment", back_populates="contract")
    insurance_package = relationship("InsurancePackage", backref="contracts")

    def to_dict(self, save_fs=None):
        dict_data = super().to_dict()
        dict_data["status"] = self.status.name if isinstance(self.status, Status) else self.status
        dict_data["group"] = self.group.to_dict() if self.group else None
        dict_data["underwriter"] = self.underwriter.to_dict() if self.underwriter else None
        dict_data["insurance_package"] = self.insurance_package.to_dict() if self.insurance_package else None
        dict_data["amendments"] = [amendment.to_dict() for amendment in self.amendments if amendment.status == "APPROVED"] if self.amendments else []
        dict_data["contract_members"] = [contract_member.to_dict() for contract_member in self.contract_members]
        return dict_data


