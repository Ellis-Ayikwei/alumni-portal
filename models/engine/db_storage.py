#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.basemodel import BaseModel, Base

from models.audit_trails import AuditTrails

from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from configs.sqlEngineConfig import db_url
from sqlalchemy.orm import scoped_session, sessionmaker

from models.client import Client
from models.coach import Coach
from models.exercise import Exercise
from models.fitness_goal import FitnessGoal
from models.meal_plan import MealPlan
from models.muscle_group import MuscleGroup
from models.post import Post
from models.user import User
from models.workout import Workout
from models.workout_level import WorkoutLevel
from models.workout_plan import WorkoutPlan

classes = {
    "BaseModel": BaseModel,
    "AuditTrails": AuditTrails,
    "User": User,
    "Client": Client,
    "Coach": Coach,
    "Workout": Workout,
    "Exercise": Exercise,
    "Post": Post,
    "MuscleGroup": MuscleGroup,
    "WorkoutPlan": WorkoutPlan,
    "WorkoutLevel": WorkoutLevel,
    "MealPlan": MealPlan,
    "FitnessGoal": FitnessGoal
}


class DBStorage:
    """interaacts with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the object with a database engine.

        This method creates a database engine using the `db_url` provided
        in the `sqlEngineConfig` module.
        The engine is then assigned to the `__engine` attribute of the object.
        """
        self.__engine = create_engine(db_url)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
    
    
    @property
    def get_session(self) -> scoped_session:
        """Returns the current database session."""
        return self.__session
