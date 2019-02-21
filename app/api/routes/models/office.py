from flask import jsonify

from app.api.responses import Responses

from app.api.routes.models.connection import CreateConnection


class GovernmentOffice(CreateConnection):
    """this initializes political office class methods"""

    def __init__(self, name=None, type=None):
        CreateConnection.__init__(self)
        if name and type:
            self.name = name
            self.type = type

    def add_political_office(self):
        """this saves political office data"""
        self.cursor.execute(
            """INSERT INTO office(name,type) VALUES(%s,%s)""", (
                self.name, self.type)
        )
        return self.find_office_by_name(self.name)

    def find_office_by_name(self, name):
        """this gets an office by name"""
        sql = """SELECT * FROM office WHERE name = '{0}'""".format(name)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def get_all_offices(self):
        """this gets all offices"""
        sql = """SELECT * FROM office"""
        self.cursor.execute(sql)
        offices = self.cursor.fetchall()
        if not offices:
            return jsonify({"message": "no created offices"}), 404
        alloffices = []
        for office in offices:
            oneoffice = {"id": office[0], "name": office[1], "type": office[2]}
            alloffices.append(oneoffice)
        return jsonify({"All offices": alloffices})

    def get_one_office(self, id):
        """this gets one office details"""
        offices = []
        self.cursor.execute("""SELECT * FROM office WHERE office_id = %s """ % id)
        data = self.cursor.fetchall()
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

    def get_specific_results(self, office_id):
        """this gets a specific office result"""
        results = []
        self.cursor.execute("""
                SELECT candidate, COUNT(candidate) AS result, office FROM votes WHERE votes.office = {} GROUP BY candidate, office;
            """.format(office_id))
        data = self.cursor.fetchall()
        if not data:
            return jsonify({"msg": "no votes casted yet"}), 404
        for result in data:
            item = {
                "candidate": result[0],
                "result": result[1],
                "office": result[2]
            }
            results.append(item)
            return jsonify({"msg": results})
