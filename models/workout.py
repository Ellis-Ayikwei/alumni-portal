from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base

class Workout(BaseModel, Base):
    __tablename__ = 'workouts'

    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    image = Column(String(255), nullable=True)
    muscle_group_id = Column(Integer, nullable=False)
    sub_muscle_group_id = Column(Integer, nullable=False)
    workout_name = Column(String(255), nullable=False)



