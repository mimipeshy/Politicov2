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

    @staticmethod
    def get_one_party(id):
        """this returns one specific party"""
        parties = []
        cur = conn.cursor()
        cur.execute("""SELECT * FROM party WHERE id = %s """ % id)
        data = cur.fetchall()
        if not data:
            return jsonify({"Message": "Party does not exist"}), 404
        for party in data:
            item = {
                "id": party[0],
                "name": party[1],
                "hqAddress": party[2],
                "logoUrl": party[3]
            }
            parties.append(item)
            return Responses.complete_response(parties)
        conn.commit()
        return parties

    @staticmethod
    def update_party(id):
        """this edits a party name"""
        partyid = id
        data = request.get_json()
        name = data['name']
        cur = conn.cursor()
        cur.execute("""SELECT id FROM party WHERE id = {}""".format(id))
        row = cur.fetchone()
        if row:
            cur.execute("""UPDATE party SET name = '{}'""".format(name))
            return make_response(jsonify({"Message": "Update successful"}))
        return make_response(jsonify({"Message": "Update failed"}), 404)