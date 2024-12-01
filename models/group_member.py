# models/groupmember.py
from email import policy
from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base
import enum
class FunctionalFitness(BaseModel, Base):
    __tablename__ = 'functional_fitness'

    definition = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    diet_recommendations = Column(String(255), nullable=False)
    goal = Column(String(255), nullable=False)
    index = Column(Integer, nullable=False)
    workout_recommendations = Column(String(255), nullable=False)

    def to_dict(self, save_fs=None):
        dict_data = super().to_dict()
        return dict_data
