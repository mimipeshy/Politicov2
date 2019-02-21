import psycopg2

from flask import make_response, jsonify

from app.api.database.db_conn import dbconn

conn = dbconn()


class Vote:
    __tablename__ = 'votes'

    def __init__(self, office, candidate, voter):
        self.office = office
        self.candidate = candidate
        self.voter = voter

    def save_vote(self):
        """
        This adds a new vote
        """
        try:
            cursor = conn.cursor()
            query = """SELECT * FROM votes WHERE candidate='{}' AND office = '{}' AND voter ='{}'""".format(self.candidate,self.office, self.voter)
            office_missing = """SELECT * FROM office WHERE office_id = '{}'""".format(self.office)
            voter_missing = """SELECT * FROM users WHERE user_id = '{}'""".format(self.voter)
            candidate_missing = """SELECT * FROM candidate WHERE id = '{}'""".format(self.candidate)

            # check if voter is registered
            cursor.execute(voter_missing)
            result_voter_missing = cursor.fetchone()
            if not result_voter_missing:
                return make_response(jsonify({"Message": "Please registerd to be able to vote"}))

            # check if voted already
            cursor.execute(query)
            voted_already = cursor.fetchone()
            if voted_already:
                return make_response(jsonify({"Message": "You have already voted"}))

            # check office
            cursor.execute(office_missing)
            result_office_missing = cursor.fetchone()
            if not result_office_missing:
                return make_response(jsonify({"Message": "No such office"}))

            #check candidate
            cursor.execute(candidate_missing)
            result_candidate_missing = cursor.fetchone()
            if not result_candidate_missing:
                return make_response(jsonify({"Message": "No such candidate"}))


            cursor.execute(
                """INSERT INTO votes(office, candidate, voter) VALUES ('{}','{}','{}') """.format(self.office, self.candidate, self.voter)
            )
            conn.commit()
            return make_response(jsonify({"Message":"Vote successfully"}))
        except (Exception, psycopg2.DatabaseError) as e:
            return make_response(jsonify({"Message": "Something went wrong" + str(e.args[0])}))



