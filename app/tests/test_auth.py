
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
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        self.client.post('/api/v2/auth/signup', content_type='application/json',
                         data=self.register_user
                                    )
        response = self.client.post('/api/v2/auth/login', headers = {
                                          'Content-Type': 'application/json'
                                      },
                                      data=json.dumps(self.login_user)
                                      )
        self.assertEqual(response.status_code, 200)
