import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Index, String,JSON
from models.basemodel import Base, BaseModel
from sqlalchemy.orm import relationship

class Amendment(Base, BaseModel):
    """
    Represents an Amendment to a member's contract
    """
    __tablename__ =  "amendments"
    
    contract_id = Column(String(60), ForeignKey('contracts.id'))
    amended_by = Column(String(60), ForeignKey('users.id'))
    change_log = Column(JSON)
    change_date = Column(DateTime, default=datetime.datetime.utcnow)
    new_values = Column(JSON)
    old_values = Column(JSON)
    
    
__table_args__ = (
        Index('ix_amendments_contract_id', 'contract_id'),
        Index('ix_amendments_amended_by', 'amended_by'),
    )