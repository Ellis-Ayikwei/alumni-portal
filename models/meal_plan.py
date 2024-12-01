from operator import index
from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from models.basemodel import BaseModel, Base

class MealPlan(BaseModel, Base):
    __tablename__ = 'meal_plans'

    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    coach_id = Column(String(60), ForeignKey('coaches.id'), nullable=False)
    client_id = Column(String(60), ForeignKey('clients.id'), nullable=True)

    coach = relationship("Coach", back_populates="meal_plans")
    client = relationship("Client", back_populates="meal_plans")
    
    __table_args__ = (
        Index("ix_meal_plans_coach_id", "coach_id"),
        Index("ix_meal_plans_client_id", "client_id"),
    )
