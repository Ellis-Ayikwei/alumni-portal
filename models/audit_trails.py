import enum
from proto import ENUM
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from models.basemodel import BaseModel, Base

class Status(enum.Enum):
    FAILED="FAILED"
    PENDING="PENDING"
    COMPLETED="COMPLETED"

class AuditTrails(BaseModel, Base):
    """Represents an audit trail"""
    __tablename__ = "audit_trails"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", backref="audit_trails", lazy="joined")
    action = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    item_audited_id = Column(String(60), nullable=True)
    
    
    def to_dict(self, save_fs=None):
        dict_o =  super().to_dict(save_fs)
        dict_o["status"] = self.status.name if isinstance(self.status, Status) else self.status
        dict_o["user"] = self.user.to_dict() if self.user else None
        return dict_o
    
    
