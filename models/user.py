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
    password_hash = Column(String(255))
    first_name = Column(String(50))
    last_name = Column(String(50))
    role = Column(Enum(UserRole), nullable=False)
    azure_id = Column(String(255), unique=True)
    is_active = Column(Boolean, default=True)

    groups = relationship("AlumniGroup", back_populates="president")
    member_profile = relationship("Member", back_populates="user", uselist=False)
    
    def __init__(self, *args, **kwargs):
        """Initialization of the user"""
        super().__init__(*args, **kwargs)
        if 'skills' in kwargs:
            self.skills = kwargs['skills']
        if 'password' in kwargs:
            self.password = bcrypt.hashpw(kwargs['password'], bcrypt.gensalt())

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password, self.password) if self.password else False


    def update_password(self, new_password: str):
        self.password = bcrypt.hashpw(new_password, bcrypt.gensalt())