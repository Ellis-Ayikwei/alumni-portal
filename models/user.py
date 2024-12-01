from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base
import bcrypt
import re

from sqlalchemy.orm import relationship

class UserRole(enum.Enum):
    CLIENT = "CLIENT"
    COACH = "COACH"
    ADMIN = "ADMIN"

class User(BaseModel, Base):
    __tablename__ = 'users'

    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    dob = Column(Date, nullable=True)



    def __init__(self, *args, **kwargs):
        """Initialization of the user"""
        super().__init__(*args, **kwargs)
        if 'password' in kwargs:
            self.password = self._hash_password(kwargs['password'])
        if 'first_name' in kwargs and 'last_name' in kwargs:
            self.full_name = f"{kwargs['first_name']} {kwargs.get('last_name', '')} {kwargs.get('other_names', '')}".strip()

    def to_dict(self, save_fs=None) -> dict:
        """Return a dictionary representation of the user, ensuring enum conversion"""
        user_dict = super().to_dict()
        
        # Convert the role enum to its string representation for serialization
        user_dict["role"] = self.role.name if isinstance(self.role, UserRole) else self.role
        
        full_name = self.full_name if self.full_name else f"{self.first_name} {self.last_name}"
        user_dict["full_name"] = full_name
        
        return user_dict

    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Ensure the password meets basic complexity requirements."""
        return bool(re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$', password))

    def verify_password(self, password: str) -> bool:
        """Verify the password against the hashed password."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')) if self.password else False
        except (ValueError, TypeError):
            return False

    def update_password(self, new_password: str):
        """Update the password with a new hash."""
        self.password = self._hash_password(new_password)

    def reset_password(self, current_password: str, new_password: str) -> bool:
        """Reset the password if the current password is verified."""
        if self.verify_password(current_password):
            self.update_password(new_password)
            return True
        return False

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash the password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
