
import unittest
import sys  # fix import errors
import os
import json

import psycopg2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.api.app import create_app
from app.api.database.db_conn import dbconn, drop_tables, create_tables



class BaseTests(unittest.TestCase):
    """This class represents the base configurations for all tests"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.conn = dbconn()
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
        self.length_name = json.dumps({
            "name": "ertt",
            "hqAddress": "koko",
            "logoUrl": "http://facebook.com/pic.jpg"

        })
        self.length_hqAddress = json.dumps({
            "name": "erttmommk",
            "hqAddress": "koko",
            "logoUrl": "http://facebook.com/pic.jpg"
        })

        self.length_type = json.dumps({
            "name": "ertmoomot",
            "type": "koko",

        })
        self.register_user = {
            "first_name": "peris",
            "last_name": "ndanu",
            "other_name": "kimeu",
            "email": "ndani@gmail.com",
            "password": "South@frica12*",
            "phone_number": "45678",
            "passportUrl": "bujuu"

        }
        self.login_user = {
            "email": "ndani@gmail.com",
            "password": "South@frica12*"

        }
        self.missing_http = json.dumps({
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
        self.validate_strings = json.dumps({
            "name": 1,
            "hqAddress": 2,
            "logoUrl": "http://mdoossd.com/pol.ko"

        })

    def get_token(self):
        """this checks a user for login"""
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                           content_type='application/json',
                           )
        response = self.client.post('/api/v2/auth/login', data=json.dumps(self.login_user),
                                      content_type='application/json',
                                      )
        self.assertEqual(response.status_code, 200)
        access_token = json.loads(response.data)['token']
        return access_token

    def tearDown(self):
        drop_tables()


if __name__ == '__main__':
    unittest.main()
