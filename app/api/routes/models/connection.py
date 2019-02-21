import datetime
from app.api.database.db_conn import dbconn, create_tables


class CreateConnection():
    '''Initializes connection to the db'''
    def __init__(self):
        self.conn = dbconn()
        create_tables()
        self.cursor = self.conn.cursor()