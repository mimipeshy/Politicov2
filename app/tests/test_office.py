import json
import unittest

from app.tests.base_test import BaseTests


class PoliticalOfficeTests(BaseTests):
    """Tests functionality of the political office endpoint"""

    def test_create_an_office(self):
        access_token = self.login_user
        response = self.client().post('/api/v2/office', data=self.add_office,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)

    def test_get_specific_office_by_id(self):
        """Tests API can get a specific party by using its id"""
        self.client().post('/api/v2/office', data=self.add_office,
                           content_type='application/json')
        response = self.client().get('/api/v2/office/1',
                                     content_type='application/json',
                                     )
        self.assertEqual(response.status_code, 200)

    def test_get_office_forbidden(self):
        self.client().post('/api/v2/office', data=self.add_office,
                          content_type='application/json')
        response = self.client().get('/api/v2/office/10',
                                     content_type='application/json',
                                     )
        self.assertEqual(response.status_code, 404)

    def test_get_all_offices(self):
        """Tests API can get all offices"""
        self.client().post('/api/v2/office', data=self.add_office,
                           content_type='application/json')
        response = self.client().get('/api/v2/office',
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()