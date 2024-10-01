from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base


class Payment(BaseModel, Base):
    __tablename__ = 'payments'

    
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False)
  

    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship("Contract")
    payer_id = Column(Integer, ForeignKey('users.id'))
    payer = relationship("User")