from sqlalchemy import Column, Integer, String
from models.basemodel import BaseModel, Base

class FitnessGoal(BaseModel, Base):
    """
    Represents a claim made under an insurance package

    Attributes:
        definition (str): The definition of fitness goal
        description (str): The description of fitness goal
        diet_recommendations (str): The diet recommendations for fitness goal
        goal (str): The goal of fitness goal
        index (int): The index of fitness goal
        workout_recommendations (str): The workout recommendations for fitness goal
    """
    __tablename__ = 'fitness_goals'

    definition = Column(String(1000), nullable=False)
    description = Column(String(500), nullable=False)
    diet_recommendations = Column(String(5000), nullable=False)
    name = Column(String(255), nullable=False)
    workout_recommendations = Column(String(2000), nullable=False)
