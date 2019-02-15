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

    @staticmethod
    def get_all_offices():
        """this gets all offices"""
        cursor = conn.cursor()
        sql = """SELECT * FROM office"""
        cursor.execute(sql)
        offices = cursor.fetchall()
        if not offices:
            return jsonify({"message": "no created offices"}), 404
        alloffices = []
        for office in offices:
            oneoffice = {}
            oneoffice["id"] = office[0]
            oneoffice["name"] = office[1]
            oneoffice["type"] = office[2]
            alloffices.append(oneoffice)
            # conn.commit()
            print(office[0])
        return jsonify({"All offices": alloffices})

    @staticmethod
    def get_one_office(id):
        """this gets one office details"""
        offices = []
        cur = conn.cursor()
        cur.execute("""SELECT * FROM office WHERE office_id = %s """ % id)
        data = cur.fetchall()
        if not data:
            return jsonify({"msg": "No offices created yet"}), 404
        for office in data:
            item = {
                "office_id": office[0],
                "name": office[1],
                "type": office[2]
            }
            offices.append(item)
        return jsonify({"msg": offices})