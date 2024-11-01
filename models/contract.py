from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base


class ContractStatus(enum.Enum):
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
    signed_date = Column(DateTime, default=datetime.now)
    status = Column(Enum(ContractStatus), default=ContractStatus.INACTIVE, nullable=False)
    underwriter_id = Column(String(60), ForeignKey('users.id'))
    insurance_package_id = Column(String(60), ForeignKey('insurance_packages.id', ondelete="SET NULL"), nullable=True)
    description = Column(String(255), nullable=True)
    policy_number = Column(String(100), nullable=True)
    
    # Relationships
    group = relationship("AlumniGroup", back_populates="contract")
    contract_members = relationship("ContractMember", back_populates="contract")
    underwriter = relationship("User", backref="contracts")
    amendments = relationship("Amendment", backref="contract")
    insurance_package = relationship("InsurancePackage", backref="contracts")


