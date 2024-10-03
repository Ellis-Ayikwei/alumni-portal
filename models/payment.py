from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base

class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Payment(BaseModel, Base):
    __tablename__ = 'payments'

    
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    status = Column(Enum(PaymentStatus), default= PaymentStatus.PENDING, nullable=False)
  

    contract_id = Column(String(60), ForeignKey('contracts.id'))
    contract = relationship("Contract")
    payer_id = Column(String(60), ForeignKey('users.id'))
    payer = relationship("User")
    
    
    def to_dict(self):
        dict_data = super().to_dict()
        
        if isinstance(self.status, PaymentStatus):
            dict_data["status"] = self.status.name
        else:
            dict_data["status"] = self.status

        return dict_data
        
    