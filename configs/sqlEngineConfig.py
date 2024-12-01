import sqlalchemy
from sqlalchemy import create_engine
"""Instantiate a DBStorage object"""
# AP_MYSQL_USER = "Ellis"
# #the passord is "@Toshib12345678" but in the sqlalchemy its seen as url == @ => %40
# AP_MYSQL_PWD = "%40Toshib12345678" 
# AP_MYSQL_HOST = "localhost"
# AP_MYSQL_DB = "alumni_portal_v1"
# AP_MYSQL_PORT = 3306


AP_MYSQL_USER = "myadmin"
#the passord is "@Toshib12345678" but in the sqlalchemy its seen as url == @ => %40
AP_MYSQL_PWD = "Toshib123"
AP_MYSQL_HOST = "localhost"
AP_MYSQL_DB = "flint_fitness"
AP_MYSQL_PORT = 4022

db_url = f"mysql+mysqldb://{AP_MYSQL_USER}:{AP_MYSQL_PWD}@{AP_MYSQL_HOST}:{AP_MYSQL_PORT}/{AP_MYSQL_DB}"
