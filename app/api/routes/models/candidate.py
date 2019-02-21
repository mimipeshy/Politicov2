import psycopg2

from flask import jsonify, make_response

from app.api.responses import Responses
from app.api.routes.models.connection import CreateConnection

class Candidates(CreateConnection):
    """this initializes political office class methods"""

    def __init__(self, office=None, candidate=None):
        CreateConnection.__init__(self)
        if office and candidate:
            self.office = office
            self.candidate = candidate

    def save_candidate(self):
        try:
            sql = """SELECT * FROM users WHERE user_id = '{}'""".format(self.candidate)
            office_sql = """SELECT * FROM office WHERE office_id = '{}'""".format(self.office)
            candidate_sql = """SELECT * FROM candidate WHERE id = '{}'""".format(self.candidate)

            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if not result:
                return make_response(jsonify({"Message": "Candidate not registered"}))

            self.cursor.execute(office_sql)
            c_office = self.cursor.fetchone()
            if not c_office:
                return make_response(jsonify({"Message": "office not registered"}))

            self.cursor.execute(candidate_sql)
            c_candidate = self.cursor.fetchone()
            if c_candidate:
                return make_response(jsonify({"Message": "Candidate already registered for office"}))
            self.cursor.execute(
                """INSERT INTO candidate(candidate, office) VALUES(%s,%s)""",
                (self.candidate, self.office))
            return make_response(jsonify({"Message": "Candidate Added succesfully",
                                          "candidate_id": self.candidate,
                                          "office_id": self.office}))
        except (Exception, psycopg2.DatabaseError) as e :
            return make_response(jsonify({"Message":"Something went wrong" + str(e.args[0])}))



