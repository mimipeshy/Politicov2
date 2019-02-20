import unittest
import sys  # fix import errors
import os
import json

import psycopg2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.api.app import create_app
from app.api.database.db_conn import dbconn, drop_tables, create_tables

conn = dbconn()


class BaseTests(unittest.TestCase):
    """This class represents the base configurations for all tests"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        with self.app.app_context():
            create_tables()

        self.add_party = json.dumps({
            "name": "maendeleo",
            "hqAddress": "kilimani",
            "logoUrl": "http://facebook.com/pic.jpg"

        })
        self.update_party = json.dumps({
            "name": "chama cha maendeleo"
        })
        self.empty_party_name = json.dumps({
            "name": "",
            "hqAddress": "koko",
            "logoUrl": "http://facebook.com/pic.jpg"
        })
        self.empty_logoUrl = json.dumps({
            "name": "wazee united",
            "hqAddress": "kokoo",
            "logoUrl": " "

        })
        self.empty_hqAddress = json.dumps({
            "name": "wazee united",
            "hqAddress": "",
            "logoUrl": "http://facebook.com/pic.jpg "

        })
        self.add_office = json.dumps({
            "name": "governnemt",
            "type": "senate"
        })
        self.length_name= json.dumps({
            "name":"ertt",
            "hqAddress": "koko",
            "logoUrl": "http://facebook.com/pic.jpg"

        })
        self.length_hqAddress = json.dumps({
             "name":"erttmommk",
            "hqAddress": "koko",
            "logoUrl": "http://facebook.com/pic.jpg"
        })

        self.length_type= json.dumps({
             "name":"ertmoomot",
            "type": "koko",

        })
        self.missing_http= json.dumps({
            "name": "erttmommk",
            "hqAddress": "kokmokoo",
            "logoUrl": "mdoossd"

        })
        self.missing_body = json.dumps({
            "name": "erttmommk",
            "hqAddress": "kokmokoo",
            "logoUrl": "http://mdoossd"

        })
        self.missing_path = json.dumps({
            "name": "erttmommk",
            "hqAddress": "kokmokoo",
            "logoUrl": "http://mdoossd.com"

        })
        self.validate_strings= json.dumps({
            "name": 1,
            "hqAddress": 2,
            "logoUrl": "http://mdoossd.com/pol.ko"

        })
        self.add_new_user= json.dumps({
            "first_name":"test",
            "last_name":"testname",
            "other_name":"testother",
            "email":"test@gmail.com",
            "phone":"1234",
            "password":"testing",
            "passportUrl":"pic/jpg",
            "is_admin":"False"

        })
        self.login= json.dumps({
            "email":"test@gmail.com",
            "password":"testing"
        })
        # self.header = {"content-type": "application/json"}
        # # login the admin
        # response = self.client().post("/api/v2/auth/login", data=json.dumps(self.login), headers=self.header)
        # # create the authentication headers
        # self.authHeaders = {"content-type": "application/json"}
        # # put the bearer token in the header
        # result = json.loads(response.data.decode())
        # print({"nvjnfvjndivnd": result})
        # self.authHeaders['Authorization'] = 'Bearer ' + result['token']

    def register_user(self, first_name, last_name, other_name, email, phone, password, passportUrl, is_admin):
        """Register user with dummy data"""
        return self.client().post(
            '/api/v2/auth/signup',
            data= json.dumps (dict(
                first_name = first_name,
                last_name = last_name,
                other_name = other_name,
                email= email,
                phone= phone,
                password= password,
                passportUrl= passportUrl,
                is_admin= is_admin
            )))


    def login_user(self, email, password):
        """Register user with dummy data"""
        return self.client().post(
            '/api/v2/auth/login',
            content_type='application/json',
            data=json.dumps(dict(
                email=email,
                password=password)))

    def user_token_get(self):
        self.register_user(first_name="peris",last_name="ndanu",other_name="kimeu",email="perisndanu@gmail.com",password="South@frica1",phone="1234567890",passportUrl="pic/jpg",is_admin=True)
        data = self.login_user(email="perisndanu@gmail.com", password="South@frica1")
        access_token = json.loads(data.data.decode())['token']
        print(access_token)
        # return access_token

    # def tearDown(self):
    #     drop_tables()


