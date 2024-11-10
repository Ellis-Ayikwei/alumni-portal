import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Index, String, JSON, Enum
from models.basemodel import Base, BaseModel
from sqlalchemy.orm import relationship
import enum

# Enum for Amendment Status
class AmendmentStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Amendment(Base, BaseModel):
    """
    Represents an Amendment to a member's contract.
    The status of an amendment determines whether it has been approved or rejected.
    """
    __tablename__ = "amendments"

    contract_id = Column(String(60), ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="amendments")
    amended_by = Column(String(60), ForeignKey('users.id'))
    change_log = Column(JSON)
    change_date = Column(DateTime, default=datetime.datetime.utcnow)
    new_values = Column(JSON)
    old_values = Column(JSON)
    status = Column(Enum(AmendmentStatus), default=AmendmentStatus.PENDING, nullable=False)
    approved_by = Column(String(60), ForeignKey('users.id'), nullable=True)
    approval_date = Column(DateTime, nullable=True)

__table_args__ = (
    Index('ix_amendments_contract_id', 'contract_id'),
    Index('ix_amendments_amended_by', 'amended_by'),
    Index('ix_amendments_status', 'status'),
)



