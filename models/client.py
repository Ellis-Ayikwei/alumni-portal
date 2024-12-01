from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from models import meal_plan
from models.basemodel import BaseModel, Base


class Client(BaseModel, Base):
    __tablename__ = 'clients'

    user_id = Column(String(60), ForeignKey('users.id'), index=True)
    goal = Column(String(255), nullable=True)

    # Establish relationship to the 'User' model
    user = relationship("User")

    # Relationship to the coach the client is assigned to
    coach_id = Column(String(60), ForeignKey('coaches.user_id'), nullable=True)
    coach = relationship("Coach")

    meal_plans = relationship("MealPlan", back_populates="client")
    
    
    __table__args__ = (
        Index('client_user_id_idx', 'user_id'),
    )
    
