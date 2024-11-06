# models/groupmember.py
from sqlalchemy import Column, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base
import enum

class Status(enum.Enum):
    PENDING = "PENDING"
    DISAPPROVED = "DISAPPROVED"
    APPROVED = "APPROVED"

class GroupMember(BaseModel, Base):
    __tablename__ = 'group_members'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False, unique=True)
    added_by = Column(String(60), ForeignKey('users.id'), nullable=True)
    group_id = Column(String(60), ForeignKey('alumni_groups.id'), nullable=False)
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    is_approved = Column(Boolean, default=False)
    is_president = Column(Boolean, default=False, nullable=True)

    # Relationships
    user_info = relationship("User", back_populates="group_memberships", foreign_keys=[user_id])
    added_by_user = relationship("User", foreign_keys=[added_by])
    group = relationship("AlumniGroup", back_populates="members", foreign_keys=[group_id])
    beneficiaries = relationship("Beneficiary", back_populates="group_members")

    def to_dict(self):
        dict_data = super().to_dict()
        dict_data["status"] = self.status.name if isinstance(self.status, Status) else self.status
        return dict_data

    def set_isApproved(self):
        self.is_validated = True

    def handle_president_removal(self):
        if self.is_president:
            alumni_group = self.group
            alumni_group.president_user_id = None
            alumni_group.president = None
            self.is_president = False
