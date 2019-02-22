import psycopg2

from flask import make_response, jsonify


from app.api.routes.models.connection import CreateConnection



class Vote(CreateConnection):
    __tablename__ = 'votes'

    def __init__(self, office, candidate, voter):
        CreateConnection.__init__(self)
        self.office = office
        self.candidate = candidate
        self.voter = voter

    def save_vote(self):
        """
        This adds a new vote
        """
        try:
            query = """SELECT * FROM votes WHERE candidate='{}' AND office = '{}' AND voter ='{}'""".format(self.candidate,self.office, self.voter)
            office_missing = """SELECT * FROM office WHERE office_id = '{}'""".format(self.office)
            voter_missing = """SELECT * FROM users WHERE user_id = '{}'""".format(self.voter)
            candidate_missing = """SELECT * FROM candidate WHERE id = '{}'""".format(self.candidate)

            # check if voter is registered
            self.cursor.execute(voter_missing)
            result_voter_missing = self.cursor.fetchone()
            if not result_voter_missing:
                return make_response(jsonify({"Message": "Please register to be able to vote"}),404)

            # check if voted already
            self.cursor.execute(query)
            voted_already = self.cursor.fetchone()
            if voted_already:
                return make_response(jsonify({"Message": "You have already voted"}),404)

            # check office
            self.cursor.execute(office_missing)
            result_office_missing = self.cursor.fetchone()
            if not result_office_missing:
                return make_response(jsonify({"Message": "No such office"}),404)

            #check candidate
            self.cursor.execute(candidate_missing)
            result_candidate_missing = self.cursor.fetchone()
            if not result_candidate_missing:
                return make_response(jsonify({"Message": "No such candidate"}),404)


            self.cursor.execute(
                """INSERT INTO votes(office, candidate, voter) VALUES ('{}','{}','{}') """.format(self.office, self.candidate, self.voter)
            )
            return make_response(jsonify({"Message":"Voted successfully"}),200)
        except (Exception, psycopg2.DatabaseError) as e:
            return make_response(jsonify({"Message": "Something went wrong" + str(e.args[0])}))



