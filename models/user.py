from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base
import bcrypt


class UserRole(enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    REGULAR = "REGULAR"
    UNDERWRITER = "UNDERWRITER"
    PREMIUM_ADMIN = "PREMIUM_ADMIN"
    SALES = "SALES"
    MEMBER = "MEMBER"

class User(BaseModel, Base):
    __tablename__ = 'users'

    
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255))
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(Enum(UserRole), default= UserRole.REGULAR, nullable=False)
    azure_id = Column(String(255), unique=True)
    is_active = Column(Boolean, default=True)

    groups = relationship("AlumniGroup", back_populates="president")
    group_member_id = Column(String(60), ForeignKey('group_members.id'))
    # member_profile = relationship("GroupMember", backref="users", uselist=False, foreign_keys="[GroupMember.user_id]")
    
    def __init__(self, *args, **kwargs):
        """Initialization of the user"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            encoded_password = kwargs['password'].encode('utf-8')
            self.password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password, self.password) if self.password else False


    def update_password(self, new_password: str):
        self.password = bcrypt.hashpw(new_password, bcrypt.gensalt())



    def to_dict(self):
        """Return a dictionary representation of the user, ensuring enum conversion"""
        dict_rep = super().to_dict()
        
        # Convert the role enum to its string representation for serialization
        if isinstance(self.role, UserRole):
            dict_rep["role"] = self.role.name
        else:
            dict_rep["role"] = self.role
        
        return dict_rep