from .base_test import BaseTests
import json


#
class AuthTests(BaseTests):
    """Tests functionality of the political endpoint"""

    def test_user_registration(self):
        """this checks a user for login"""
        response = self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                                    content_type='application/json',
                                    )
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "User created successfully")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.content_type == 'application/json')

    def test_extra_field_registration(self):
        """this checks for extra fields during user registration"""
        response = self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user_extra),
                                    content_type='application/json',
                                    )
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "extra is not a valid key")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.content_type == 'application/json')

    def test_duplicate_user_registration(self):
        """ checks user cannot register twice with same details"""
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                         content_type='application/json',
                         )
        response = self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                                    content_type='application/json',
                                    )
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "User already exists, please login")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.content_type == 'application/json')

    def test_user_login(self):
        """Test user logs in Successfully"""
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                         content_type='application/json',
                         )
        response = self.client.post('/api/v2/auth/login', data=json.dumps(self.login_user),
                                    content_type='application/json'
                                    )
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_login_wrong_password(self):
        """tests user logging in with wrong password"""
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                         content_type='application/json',
                         )
        response = self.client.post('/api/v2/auth/login', data=json.dumps(self.wrong_passwrd),
                                    content_type='application/json'
                                    )
        self.assertTrue(response.content_type == 'application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "Wrong Password!")
        self.assertEqual(response.status_code, 404)

    def test_login_missing_email(self):
        """Test if user leaves email field empty"""
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                         content_type='application/json',
                         )
        response = self.client.post('/api/v2/auth/login', data=json.dumps({"email": "",
                                                                           "password": "South@frica1"}),
                                    content_type='application/json'
                                    )
        self.assertTrue(response.content_type == 'application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "Your email is missing!")
        self.assertEqual(response.status_code, 404)

    def test_login_invalid_user(self):
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                         content_type='application/json',
                         )
        response = self.client.post('/api/v2/auth/login', data=json.dumps({"email": "ndanu@gmail.com",
                                                                           "password": "South@frica1"}),
                                    content_type='application/json'
                                    )
        self.assertTrue(response.content_type == 'application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "User does not exist. Kindly register!")
        self.assertEqual(response.status_code, 404)

    def test_missing_password(self):
        """Test if user leaves password field empty"""
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                         content_type='application/json',
                         )
        response = self.client.post('/api/v2/auth/login', data=json.dumps({"email": "ndani@gmail.com",
                                                                           "password": ""}),
                                    content_type='application/json'
                                    )
        self.assertTrue(response.content_type == 'application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "Your password is missing!")
        self.assertEqual(response.status_code, 404)

    def test_invalid_email(self):
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                         content_type='application/json',
                         )
        response = self.client.post('/api/v2/auth/login', data=json.dumps({"email": "ndanugmail.com",
                                                                           "password": "South@frica1"}),
                                    content_type='application/json'
                                    )
        self.assertTrue(response.content_type == 'application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "Your email is invalid! Kindly recheck your email.")
        self.assertEqual(response.status_code, 404)

    def test_empty_login_fields(self):
        self.client.post('/api/v2/auth/signup', data=json.dumps(self.register_user),
                         content_type='application/json',
                         )
        response = self.client.post('/api/v2/auth/login', data=json.dumps({}),
                                    content_type='application/json'
                                    )
        self.assertTrue(response.content_type == 'application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data["Data"]['Message'] == "Please provide for all the fields. Missing field:  email, password")
        self.assertEqual(response.status_code, 400)


