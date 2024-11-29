from sqlalchemy import JSON, Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base
from models.payment import Payment

class InvoiceStatus(enum.Enum):
    DRAFT = "DRAFT"
    ISSUED = "ISSUED"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"

class InvoiceType(enum.Enum):
    GROUP_CONTRACT = "GROUP_CONTRACT"
    INDIVIDUAL_CONTRACT = "INDIVIDUAL_CONTRACT"
   

class Invoice(BaseModel, Base):
    """
    Comprehensive Invoice Model
    """
    __tablename__ = 'invoices'

    
    # Relationship References
    group_id = Column(String(60), ForeignKey('alumni_groups.id'), nullable=True)
    contract_id = Column(String(60), ForeignKey('contracts.id', ondelete="SET NULL"), nullable=True)
    billed_user_id = Column(String(60), ForeignKey('users.id'))  # Billed user
    insurance_package_id = Column(String(60), ForeignKey('insurance_packages.id'), nullable=True)
    
    # Invoice Details
    invoice_number = Column(String(50), unique=True, nullable=False)
    
    # Financial Details
    total_amount = Column(Float, default=0.0,nullable=False)
    total_paid = Column(Float, default=0, nullable=False)
    
    # Status Tracking
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    invoice_type = Column(Enum(InvoiceType), nullable=False)
    

    # Date Tracking
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    paid_date = Column(DateTime)
    
    # Additional Metadata
    description = Column(String(255))
    
    # Audit Fields
    created_by = Column(String(60), ForeignKey('users.id'), nullable=True)
    last_updated_by = Column(String(60), ForeignKey('users.id'), nullable=True)
    
    # Relationships
    group = relationship('AlumniGroup')
    contract = relationship('Contract')
    billed_user = relationship('User', foreign_keys=[billed_user_id])
    created_by_user = relationship('User', foreign_keys=[created_by])
    last_updated_by_user = relationship('User', foreign_keys=[last_updated_by])
    
    insurance_package = relationship('InsurancePackage')

    # One-to-Many relationship with Invoice Line Items
    payments = relationship('Payment', back_populates='invoice', foreign_keys=[Payment.invoice_id])


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from models import storage

        if "total_amount" in kwargs:
            print("the total amounts", kwargs["total_amount"])
            amount = float(kwargs["total_amount"])
            if self.validate_amount(amount):
                
                print("the total amounts v", kwargs["total_amount"])
                self.total_amount = amount

        if not kwargs.get("invoice_number"):
            invoice = storage.get_session.query(Invoice).order_by(Invoice.invoice_number.desc()).first().invoice_number if storage.get_session.query(Invoice).count() > 0 else 1
            new_invoice_ = int(invoice.split("-")[1]) + 1 if invoice else 1
            self.invoice_number = f"INV-{new_invoice_:06d}"
        
        
        print("the invoice number", self.total_amount)
        
    def to_dict(self, save_fs=None):
        dict_data = super().to_dict()
        dict_data["status"] = self.status.name if isinstance(self.status, InvoiceStatus) else self.status
        dict_data["invoice_type"] = self.invoice_type.name if isinstance(self.invoice_type, InvoiceType) else self.invoice_type
        dict_data["billed_user"] = {"full_name": self.billed_user.full_name, "email": self.billed_user.email, "phone": self.billed_user.phone, "id": self.billed_user.id, "role": self.billed_user.role.name} if self.billed_user else None
        if self.group:
            current_contract = {"id": self.group.current_contract.id, "name": self.group.current_contract.name} if self.group.current_contract else None
            insurance_package = {"id": self.group.insurance_package.id, "name": self.group.insurance_package.name} if self.group.insurance_package else None
            dict_data["group"] = {"id": self.group.id, "name": self.group.name, "currrent_contract": current_contract, "insurance_package": insurance_package}
        else:
            dict_data["group"] = None
        # dict_data["group"] = self.group.to_dict() if self.group else None
        # dict_data["contract"] = self.contract.to_dict() if self.contract else None
        # dict_data["user"] = self.user.to_dict() if self.user else None
        return dict_data



    @staticmethod
    def validate_amount(amount):
        print("the amount", amount)
        if amount <= 0:
            raise ValueError("Amount must be a positive value.")



    def generate_invoice(self):
        """Generate a simple invoice message to send to the users"""
        message = f"Invoice Number: {self.invoice_number}\n"
        message += f"Bill To: {self.billed_user.full_name}\n"
        message += f"Group: {self.group.name}\n"
        message += f"Insurance Package: {self.insurance_package.name}\n"
        message += f"Total Amount: {self.total_amount}\n"
        message += f"Due Date: {self.due_date.strftime('%Y-%m-%d')}\n"
        return message
