from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base


class MuscleGroup(BaseModel, Base):
    __tablename__ = 'muscle_groups'

    name = Column(String(128), nullable=False)
    description = Column(String(255) , nullable=True)
