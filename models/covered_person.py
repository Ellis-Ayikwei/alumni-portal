from sqlalchemy import Column, Index, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base

class CoveredPersonType(enum.Enum):
    ALUMNI_MEMBER = "ALUMNI_MEMBER"
    SPOUSE = "SPOUSE"
    PARENT = "PARENT"
    PARENT_IN_LAW = "PARENT_IN_LAW"
    GUARDIAN = "GUARDIAN"
    SIBLING = "SIBLING"
    CHILD = "CHILD"

class CoveredPerson(BaseModel, Base):
    """
    Represents a person covered under the insurance package

    Attributes:
        alumni_member_id (str): The id of the alumni member
        type (CoveredPersonType): The type of covered person
        name (str): The name of the covered person
    """
    __tablename__ = 'covered_persons'

    alumni_member_id = Column(String(60), ForeignKey('alumni_members.id'))
    type = Column(Enum(CoveredPersonType), nullable=False)
    name = Column(String(100), nullable=False)

    # Relationships
    alumni_member = relationship("AlumniMember", back_ref="covered_persons")
   
   
   
   
__table_args__ = (
        Index('ix_covered_persons_alumni_member_id', 'alumni_member_id'),
    )