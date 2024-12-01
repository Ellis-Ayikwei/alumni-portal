from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
from models.basemodel import BaseModel, Base


class Exercise(BaseModel, Base):
    """
    Represents an exercise

    Attributes:
        name (str): Exercise name
        gif_url (str): Exercise gif URL
        local_png (str): Exercise local PNG path
        local_url (str): Exercise local URL
        metric (str): Exercise metric
        target (str): Exercise target
        equipment (str): Exercise equipment
        body_part (str): Exercise body part
    """
    __tablename__ = 'exercises'

    name = Column(String(100), nullable=False)
    gif_url = Column(String(255), nullable=False)
    local_png = Column(String(255), nullable=False)
    local_url = Column(String(255), nullable=False)
    metric = Column(String(50), nullable=False)
    target = Column(String(50), nullable=False)
    equipment = Column(String(50), nullable=False)
    body_part = Column(String(50), nullable=False)

