import enum
from sqlalchemy import Column, Index, String, Float, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base
from datetime import datetime

class ClaimStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Claim(BaseModel, Base):
    """
    Represents a claim made under an insurance package

    Attributes:
        alumni_member_id (str): The id of the alumni member
        benefit_id (str): The id of the benefit
        amount (float): The claim amount
        status (ClaimStatus): The status of the claim
        claim_date (datetime): The date the claim was made
    """
    __tablename__ = 'claims'

    alumni_member_id = Column(String(60), ForeignKey('group_members.id'))
    benefit_id = Column(String(60), ForeignKey('benefits.id'))
    amount = Column(Float, nullable=False)
    status = Column(Enum(ClaimStatus), default=ClaimStatus.PENDING, nullable=False)
    claim_date = Column(DateTime, default=datetime.now, nullable=False)

    # Relationships
    alumni_member = relationship("GroupMember", backref="claims")
    benefit = relationship("Benefit")
    
    
    
__table_args__ = (
        Index('ix_claims_alumni_member_id', 'alumni_member_id'),
        Index('ix_claims_status', 'status'),
    )