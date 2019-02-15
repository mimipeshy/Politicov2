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

    @staticmethod
    def get_all_parties():
        """this returns all parties"""
        cursor = conn.cursor()
        sql = "SELECT * FROM party"
        cursor.execute(sql)
        parties = cursor.fetchall()
        if not parties:
            return jsonify({"Message": "No created parties"}), 404
        allparties = []
        for party in parties:
            oneparty = {}
            oneparty["id"] = party[0]
            oneparty["name"] = party[1]
            oneparty["hqAddress"] = party[2]
            oneparty["logoUrl"] = party[3]

            allparties.append(oneparty)
        return jsonify({"Parties": allparties})
