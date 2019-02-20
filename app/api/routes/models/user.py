from datetime import datetime, timedelta

import jwt
from flask import jsonify, current_app
from app.api.database.db_conn import dbconn
import app.api.validations.validation as validate
import app.api.responses as errors

conn = dbconn()


class UserModel:
    __tablename__ = 'users'

    def __init__(self, first_name, last_name, other_name, email, phone, password, passportUrl, is_admin):
        self.email = email
        self.password_hash = validate.hash_password(password)
        self.admin = is_admin
        self.fname = first_name
        self.lname = last_name
        self.othername = other_name
        self.phone = phone
        self.passport = passportUrl
        print(self.password_hash)

    def save(self, is_admin):
        """this adds a new user"""
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users(fname,lname, othername,email,phone,password,passUrl,is_admin) VALUES(%s,%s,%s,%s,%s,"
            "%s,%s,%s)", (
                self.fname, self.lname, self.othername, self.email, self.phone, self.password_hash, self.passport, is_admin)
        )
        cursor.execute("SELECT user_id FROM users WHERE email = %s", (self.email,))
        row = cursor.fetchone()
        conn.commit()

    @staticmethod
    def get_one_by_email(email):
        """this gets a user by use of email"""
        cur = conn.cursor()
        sql = """SELECT * FROM users WHERE email = '{0}'""".format(email)
        cur.execute(sql)
        result = cur.fetchone()
        conn.commit()
        return result

    @staticmethod
    def get_one_by_id(user_id):
        """this gets a user by use of id"""
        cur = conn.cursor()
        sql = """SELECT * FROM users WHERE user_id = '{}'""".format(user_id)
        cur.execute(sql)
        result = cur.fetchone()
        conn.commit()
        return result

    @staticmethod
    def fetch_user_id(email):
        """Method returns the user's id by querying the email"""
        cur = conn.cursor()
        query = """SELECT user_id FROM users WHERE email='{}'""" .format(email)
        cur.execute(query)
        result = cur.fetchone()
        conn.commit()
        return result

    @staticmethod
    def get_password(email):
        """this checks if password is same to given email"""
        cur = conn.cursor()
        sql = """SELECT password FROM users WHERE email = '%s'""" % email
        cur.execute(sql)
        row = cur.fetchone()
        if row is None:
            return None
        conn.commit()
        return row

    @staticmethod
    def get_all_users():
        """this returns all users"""
        cur = conn.cursor()
        cur.execute("""SELECT * FROM users """)
        result = cur.fetchall()

        if result:
            message = "No users exist in the database"
            response = jsonify({"message": message})
        else:
            users = []
            for user in result:
                single_user = {}
                single_user['user_id'] = user[0]
                single_user['fname'] = user[1]
                single_user['lname'] = user[2]
                single_user['othername'] = user[3]
                single_user['password'] = user[4]
                single_user['is_admin'] = user[5]
                users.append(single_user)
            response = users
        return response

    @staticmethod
    def fetch_role(user_id):
        """Method to return the user's role"""
        cur = conn.cursor()
        cur.execute("""SELECT is_admin FROM users WHERE user_id='%s'""" % user_id)
        row = cur.fetchone()
        cur.close()
        return row

