from flask import jsonify, make_response, request
from app.api.responses import Responses


from app.api.routes.models.connection import CreateConnection


class PoliticalParty(CreateConnection):
    """this initializes political party class methods"""

    def __init__(self, name=None, hqAddress=None, logoUrl=None):
        CreateConnection.__init__(self)
        if name and hqAddress and logoUrl:
            self.name = name
            self.hqAddress = hqAddress
            self.logoUrl = logoUrl

    def save(self):
        """this adds a new party"""
        self.cursor.execute(
            """INSERT INTO party(name,hqAddress, logoUrl) VALUES(%s,%s,%s) """, (
                self.name, self.hqAddress, self.logoUrl)
        )
        return self.find_party_by_name(self.name)

    def find_party_by_name(self, name):
        """this gets a party by name"""
        sql = """SELECT * FROM party WHERE name = '{0}'""".format(name)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        return result

    def get_all_parties(self):
        """this returns all parties"""
        sql = "SELECT * FROM party"
        self.cursor.execute(sql)
        parties = self.cursor.fetchall()
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
        return jsonify({"Parties": allparties}),200

    def get_one_party(self, id):
        """this returns one specific party"""
        parties = []
        self.cursor.execute("""SELECT * FROM party WHERE id = %s """ % id)
        data = self.cursor.fetchall()
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
        return parties

    def update_party(self, id):
        """this edits a party name"""
        try:
            partyid = id
            data = request.get_json()
            name = data['name']
            self.cursor.execute("""SELECT id FROM party WHERE id = {}""".format(id))
            row = self.cursor.fetchone()
            if row:
                self.cursor.execute("""UPDATE party SET name = '{}'""".format(name))
                return make_response(jsonify({"Message": "Update successful"}),200)
        except Exception:
            return make_response(jsonify({"Message": "Update failed"}), 400)

    def delete_party(self, id):
        """this deletes a party"""
        sql = """DELETE FROM party WHERE id = %(id)s"""
        data = {"id": int(id)}
        self.cursor.execute(sql, data)

    def find_party_by_id(self, id):
        """this gets a party by id"""
        sql = """SELECT * FROM party WHERE id = '{0}'""".format(id)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        return result