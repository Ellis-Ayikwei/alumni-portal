from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime
import enum
from models import payment
from models.amendment import AmendmentStatus
from models.basemodel import BaseModel, Base
import json

from models.contract_member import ContractMember

class Status(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    LOCKED = "LOCKED"
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
    
    # Relationships
    payments = relationship("Payment", back_populates="contract")
    group = relationship("AlumniGroup", back_populates="contracts", foreign_keys=[group_id])
    contract_members = relationship("ContractMember", back_populates="contract", cascade="all, delete-orphan")
    underwriter = relationship("User", backref="contracts")
    amendments = relationship("Amendment", back_populates="contract")
    insurance_package = relationship("InsurancePackage", backref="contracts")

    def to_dict(self, save_fs=None):
        dict_data = super().to_dict()
        dict_data["status"] = self.status.name if isinstance(self.status, Status) else self.status
        dict_data["group"] = self.group.to_dict() if self.group else None
        dict_data["underwriter"] = self.underwriter.to_dict() if self.underwriter else None
        dict_data["insurance_package"] = self.insurance_package.to_dict() if self.insurance_package else None
        dict_data["amendments"] = [{
                                    "name": amendment.name,
                                    "new_values": amendment.new_values,
                                    "old_values": amendment.old_values,
                                    "approved_by": amendment.approved_by.to_dict() if amendment.approved_by else None,
                                    "amended_by": amendment.amended_by.to_dict() if amendment.amended_by else None,
                                    "status": amendment.status.name if isinstance(amendment.status, AmendmentStatus) else amendment.status,
                                    "change_date": amendment.change_date.isoformat()} for amendment in self.amendments] if self.amendments else None
        dict_data["contract_members"] = [member.to_dict() for member in self.contract_members] if self.contract_members else None
        return dict_data

    
    
    def lock_contract(self) -> None:
        """Lock the contract, preventing further changes.

        This method sets the contract status to LOCKED and populates the contract_members list with the members of the group that have been approved and are part of the group.
        """
        if self.group:
            approved_group_members = [
                member
                for member in self.group.members
                if member.to_dict()["status"] == "APPROVED" and member.to_dict()["is_approved"] == True or member.to_dict().status == "APPROVED" and member.to_dict().is_approved and member.group_id not in [contract.group_id for contract in self.group.contracts]
            ]
            
            for group_member in approved_group_members:
                if group_member.user_id in [contract_member.user_id for contract_member in self.contract_members]:
                    continue
                ContractMember(
                    contract_id=self.id,
                    user_id=group_member.user_id,
                    group_member_id=group_member.id
                ).save()
            self.status = "LOCKED"
    def __repr__(self):
        return json.dumps(self.to_dict(), default=lambda o: o.__dict__, indent=4)
