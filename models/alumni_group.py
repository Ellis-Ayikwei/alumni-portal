from sqlalchemy import Column, Index, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base

class Status(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"
    TERMINATED = "TERMINATED"
    
class AlumniGroup(BaseModel, Base):
    __tablename__ = 'alumni_groups'

    id = Column(String(60), primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    school = Column(String(100), nullable=False)
    status = Column(Enum(Status), default=Status.ACTIVE, nullable=False)
    package_id = Column(String(60), ForeignKey('insurance_packages.id', ondelete="SET NULL"), nullable=True)
    
    # Foreign key to reference the president user
    president_user_id = Column(String(60), ForeignKey('users.id'))
    
    # Relationship to user acting as president
    president = relationship("User", back_populates="groups_as_president", foreign_keys=[president_user_id])
    
    group_members = relationship("GroupMember", backref="groups")
    contract = relationship("Contract", back_populates="group")
    insurance_package = relationship("InsurancePackage", back_populates="groups")

    __table_args__ = (
        Index('ix_alumni_groups_name', 'name'),
        Index('ix_alumni_groups_school', 'school'),
        Index('ix_alumni_groups_status', 'status'),
    )