import sqlalchemy
from sqlalchemy import create_engine
"""Instantiate a DBStorage object"""
SC_MYSQL_USER = "Ellis"
#the passord is "@Toshib12345678" but in the sqlalchemy its seen as url == @ => %40
SC_MYSQL_PWD = "%40Toshib12345678" 
SC_MYSQL_HOST = "localhost"
SC_MYSQL_DB = "alumni_portal_v1"
SC_MYSQL_PORT = 3306


db_url = f"mysql+mysqldb://{SC_MYSQL_USER}:{SC_MYSQL_PWD}@{SC_MYSQL_HOST}/{SC_MYSQL_DB}"
