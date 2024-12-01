from sqlalchemy import Column, String, ForeignKey, Integer, Table, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.basemodel import BaseModel, Base

workout_plan_exercise = Table(
    'workout_plan_exercise',
    Base.metadata,
    Column('workout_plan_id', String(60), ForeignKey('workout_plans.id'), primary_key=True),
    Column('exercise_id', String(60), ForeignKey('exercises.id'), primary_key=True)
)

class WorkoutPlan(BaseModel, Base):
    __tablename__ = 'workout_plans'

    name = Column(String(100), nullable=False)  # Name of the workout plan
    description = Column(Text, nullable=True)  # Detailed description of the workout plan
    duration = Column(Integer, nullable=False)  # Duration in days or weeks
    frequency = Column(String(50), nullable=True)  # How often the plan should be followed (e.g., '3 days a week')
    target_audience = Column(String(50), nullable=True)  # Target audience, e.g., 'beginner', 'intermediate'
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key relationship with User (coach who created the plan)
    coach_id = Column(String(60), ForeignKey('coaches.id'), nullable=False)
    
    # Relationship to the User model (coach who created the plan)
    coach = relationship("Coach", foreign_keys=[coach_id])

    # One-to-many relationship with Exercise (plan can have many exercises)
    exercises = relationship("Exercise", secondary=workout_plan_exercise, backref="workout_plans", lazy="dynamic")
    
    def __init__(self, *args, **kwargs):
        """Initialization of the workout plan"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Return a dictionary representation of the workout plan"""
        workout_plan_dict = super().to_dict()
        workout_plan_dict["coach"] = self.coach.to_dict() if self.coach else None
        workout_plan_dict["exercises"] = [exercise.to_dict() for exercise in self.exercises]  # Convert exercises to dicts
        return workout_plan_dict

