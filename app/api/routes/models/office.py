from flask import jsonify

from app.api.responses import Responses
from app.api.database.db_conn import  dbconn

conn = dbconn()
offices = []


class GovernmentOffice:
    """this initializes political office class methods"""

    def __init__(self, name, type):
        self.id = len(offices) + 1
        self.name = name
        self.type = type