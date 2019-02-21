import json
import unittest

from app.tests.base_test import BaseTests
from .base_test import BaseTests


#
class AuthTests(BaseTests):
    """Tests functionality of the political endpoint"""

    def test_user_registration(self):
        """this checks a user for login"""
        response = self.client().post('/api/v2/auth/signup', data=self.register_user,
                                      content_type='application/json',
                                      )
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        response = self.client().post('/api/v2/auth/login', data=self.login_user,
                                      content_type='application/json',
                                      )
        self.assertEqual(response.status_code, 200)
