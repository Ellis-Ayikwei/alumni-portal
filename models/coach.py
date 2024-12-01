from sqlalchemy import Column, ForeignKey, Integer, String, Index
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base
from models.workout_plan import WorkoutPlan

# Create indexes to speed up queries for frequently accessed fields


class Coach(BaseModel, Base):
    __tablename__ = 'coaches'

    user_id = Column(String(60), ForeignKey('users.id'))
    specialization = Column(String(100), nullable=True)
    experience_years = Column(Integer, nullable=True)

    # Establish relationship to the 'User' model
    user = relationship("User")

    # Relationship to clients that the coach manages
    clients = relationship("Client", back_populates="coach")

    # Optionally: relationship to workout and meal plans created by the coach
    meal_plans = relationship("MealPlan", back_populates="coach")
    workout_plans = relationship("WorkoutPlan", back_populates="coach", foreign_keys=[WorkoutPlan.coach_id])

    # Indexes
    __table_args__ = (
        Index('ix_coach_id', 'id'),
        Index('ix_coach_user_id', 'user_id'),
        Index('ix_coach_specialization', 'specialization'),
    )

