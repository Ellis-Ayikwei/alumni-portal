from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from models.basemodel import BaseModel, Base


class AuditTrails(BaseModel, Base):
    """Represents an audit trail"""
    __tablename__ = "audit_trails"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", backref="audit_trails", lazy="joined")
    action = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
