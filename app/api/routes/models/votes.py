from flask import jsonify
from app.api.database.db_conn import dbconn
import app.api.validation as validate

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
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO votes(office, candidate, voter) VALUES ('{}','{}','{}') """.format(self.office, self.candidate, self.voter)
        )
        conn.commit()

    @staticmethod
    def user_voted_status(voter, office):
        """this checks if a user has already voted or not"""
        cursor = conn.cursor()
        cursor.execute(
            """SELECT voter, office FROM votes WHERE votes.voter == '{}' AND votes.office= '{}'""".format(voter,
                                                                                                          office))
        rows = cursor.fetchall()
        conn.close()

