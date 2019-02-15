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
    def add_political_office(self, name, type):
        """this saves political office data"""
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO office(name,type) VALUES(%s,%s)""", (
                name, type)
        )
        conn.commit()
        return GovernmentOffice.find_office_by_name(name)

    @staticmethod
    def find_office_by_name(name):
        """this gets an office by name"""
        cursor = conn.cursor()
        sql = """SELECT * FROM office WHERE name = '{0}'""".format(name)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
