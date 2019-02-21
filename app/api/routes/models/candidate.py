import psycopg2

from flask import jsonify, make_response

from app.api.responses import Responses
from app.api.database.db_conn import dbconn

conn = dbconn()


class Candidates:
    """this initializes political office class methods"""

    def __init__(self, office, candidate):
        self.office = office
        self.candidate = candidate

    @staticmethod
    def save_candidate(candidate, office):
        try:
            cursor = conn.cursor()
            sql = """SELECT * FROM users WHERE user_id = '{}'""".format(candidate)
            office_sql = """SELECT * FROM office WHERE office_id = '{}'""".format(office)
            candidate_sql = """SELECT * FROM candidate WHERE id = '{}'""".format(candidate)

            cursor.execute(sql)
            result = cursor.fetchone()
            if not result:
                return make_response(jsonify({"Message": "Candidate not registered"}))

            cursor.execute(office_sql)
            c_office = cursor.fetchone()
            if not c_office:
                return make_response(jsonify({"Message": "office not registered"}))

            cursor.execute(candidate_sql)
            c_candidate = cursor.fetchone()
            if c_candidate:
                return make_response(jsonify({"Message": "Candidate already registered for office"}))
            cursor.execute(
                """INSERT INTO candidate(candidate, office) VALUES(%s,%s)""",
                (candidate, office))
            conn.commit()
            conn.close()
            return make_response(jsonify({"Message": "Candidate Added succesfully",
                                          "candidate_id": candidate,
                                          "office_id": office}))
        except (Exception, psycopg2.DatabaseError) as e :
            return make_response(jsonify({"Message":"Something went wrong" + str(e.args[0])}))



