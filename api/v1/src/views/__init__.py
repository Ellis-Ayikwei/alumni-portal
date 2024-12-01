#!/usr/bin/python3
""" Blueprint for API """
import logging
from flask import Blueprint
from models import storage

# Create Blueprints
app_views = Blueprint('app_views', __name__, url_prefix='/alumni/api/v1', template_folder='../templates')
app_auth = Blueprint('app_auth', __name__, url_prefix='/alumni/api/v1/auth', template_folder='../templates')

"""Import for the views"""
from .index_bp import *
from .user_bp import *

from .execise_bp import *
from .sub_muscle_bp import *
from .muscle_group_bp import *
from .workout_bp import *
from .sub_muscle_bp import *
from .fitness_goal_bp import *
# from .achievement_bp import *
from . workout_level_bp import *
from .coach_bp import *
from .client_bp import *

