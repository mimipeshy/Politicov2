from flask import jsonify

from app.api.routes.models.connection import CreateConnection
from app.api.validations.auth_validations import AuthValidations as validate


class UserModel(CreateConnection):
    __tablename__ = 'users'

    def __init__(self, first_name=None, last_name=None, other_name=None, email=None, phone=None, password=None,
                 passportUrl=None, is_admin=None):
        CreateConnection.__init__(self)
        if first_name and last_name and other_name and email and passportUrl and password and phone and not is_admin:
            self.email = email
            self.password_hash = validate.hash_password(password)
            self.admin = is_admin
            self.first_name = first_name
            self.lname = last_name
            self.othername = other_name
            self.phone = phone
            self.passport = passportUrl
            print(self.first_name)

    def save(self):
        """this adds a new user"""
        self.cursor.execute(
            "INSERT INTO users(fname,lname, othername,email,phone,password,passUrl,is_admin) VALUES(%s,%s,%s,%s,%s,"
            "%s,%s,%s)", (
                self.first_name, self.lname, self.othername, self.email, self.phone, self.password_hash, self.passport,
                self.admin)
        )

    def get_one_by_email(self, email):
        """this gets a user by use of email"""
        sql = """SELECT * FROM users WHERE email = '{0}'""".format(email)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def get_one_by_id(self, user_id):
        """this gets a user by use of id"""
        sql = """SELECT * FROM users WHERE user_id = '{}'""".format(user_id)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def fetch_user_id(self, email):
        """Method returns the user's id by querying the email"""
        query = """SELECT user_id FROM users WHERE email='{}'""".format(email)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def get_password(self, email):
        """this checks if password is same to given email"""
        sql = """SELECT password FROM users WHERE email = '%s'""" % email
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row is None:
            return None
        return row

    def get_all_users(self):
        """this returns all users"""
        self.cursor.execute("""SELECT * FROM users """)
        result = self.cursor.fetchall()

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

    def fetch_role(self, user_id):
        """Method to return the user's role"""
        self.cursor.execute("""SELECT is_admin FROM users WHERE user_id='%s'""" % user_id)
        row = self.cursor.fetchone()
        return row
