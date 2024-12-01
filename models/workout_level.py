from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base

class WorkoutLevel(BaseModel, Base):
    __tablename__ = 'workout_levels'

    description = Column(String(255), nullable=False)
    level_name = Column(String(60), nullable=False)
    suitable_for_female = Column(Boolean, nullable=False)
    suitable_for_male = Column(Boolean, nullable=False)
    image = Column(String(255), nullable=False)

   

