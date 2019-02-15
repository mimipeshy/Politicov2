from flask import jsonify, make_response, request
from app.api.responses import Responses

from app.api.database.db_conn import dbconn

conn = dbconn()


class PoliticalParty:
    """this initializes political party class methods"""

    def __init__(self, name, hqAddress, logoUrl):
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl

    def save(self, name, hqAddress, logoUrl):
        """this adds a new party"""
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO party(name,hqAddress, logoUrl) VALUES(%s,%s,%s) """, (
                name, hqAddress, logoUrl)
        )
        conn.commit()
        return PoliticalParty.find_party_by_name(name)

    @staticmethod
    def find_party_by_name(name):
        """this gets a party by name"""
        cursor = conn.cursor()
        sql = """SELECT * FROM party WHERE name = '{0}'""".format(name)
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        return result