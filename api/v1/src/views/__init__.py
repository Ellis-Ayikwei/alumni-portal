#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint
from models import storage

app_views = Blueprint('app_views', __name__, url_prefix='/alumni/api/v1', template_folder='../templates')

"""Import for the views"""
from .index_bp import *
from .user_bp import *
from .alumni_group_bp import *
from .group_member_bp import *
from .amemdemt_bp import *
from .contract_members_bp import *
from .paymets_bp import *
from .contracts_bp import *
from .beneficiary_bp import *

