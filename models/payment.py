from click import group
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base

# Enum for payment status
class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

# Payment class definition
class Payment(BaseModel, Base):
    __tablename__ = 'payments'
    
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_method = Column(String(60), nullable=True)
    receipt_url = Column(String(255), nullable=True)
    group_id = Column(String(60), ForeignKey('alumni_groups.id'))
    
    contract_id = Column(String(60), ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="payments")
    
    group = relationship("AlumniGroup", back_populates="payments")
    payer_id = Column(String(60), ForeignKey('users.id'))
    payer = relationship("User", back_populates="payments")
    
    @staticmethod
    def validate_amount(amount):
        if amount <= 0:
            raise ValueError("Amount must be a positive value.")
    
    def __init__(self, amount, status=None, payment_method=None, receipt_url=None):
        self.validate_amount(amount)
        self.amount = amount
        self.status = status or PaymentStatus.PENDING
        self.payment_method = payment_method
        self.receipt_url = receipt_url
        self.payment_date = datetime.utcnow()
    
    def to_dict(self, save_fs=None):
        dict_data = super().to_dict()
        dict_data["status"] = self.status.name if isinstance(self.status, PaymentStatus) else self.status
        dict_data["payment_method"] = self.payment_method
        dict_data["receipt_url"] = self.receipt_url
        dict_data["payment_date"] = self.payment_date.isoformat()
        dict_data["group"] = self.group.to_dict()
        
        
        
        return dict_data
