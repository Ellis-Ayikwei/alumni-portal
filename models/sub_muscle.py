from sqlalchemy import Column, ForeignKey, Integer, String

from models.basemodel import BaseModel, Base
from sqlalchemy.orm import relationship


class SubMuscle(BaseModel, Base):
    """
    Represents the description of a submuscle

    Attributes:
        main_muscle_id (int): The id of the main muscle
        main_muscle (str): The name of the main muscle
        sub_id (int): The id of the submuscle
        sub_muscle_name (str): The name of the submuscle
        description (str): The description of the submuscle
    """
    __tablename__ = 'sub_muscles'

    main_muscle_id = Column(String(60), ForeignKey('muscle_groups.id'))
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    # Relationships
    main_muscle = relationship("MuscleGroup", backref="sub_muscles")
