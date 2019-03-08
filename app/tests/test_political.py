import json
import unittest

from app.tests.base_test import BaseTests


class PoliticalTests(BaseTests):
    """Tests functionality of the political endpoint"""

    def test_create_party(self):
        """Test API can create a party"""
        token = self.get_token()
        response = self.client.post('/api/v2/party', data=self.add_party,
                                    headers=dict(Authorization="Bearer " + token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_all_parties(self):
        """Tests API can get all parties"""
        token = self.get_token()
        self.client.post('/api/v2/party', data=self.add_party,
                         headers=dict(Authorization="Bearer " + token),
                         content_type='application/json')
        response = self.client.get('/api/v2/party',
                                   headers=dict(Authorization="Bearer " + token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_specific_by_id(self):
        """Tests API can get a specific party by using its id"""
        token = self.get_token()
        self.client.post('/api/v2/party', data=self.add_party,
                         headers=dict(Authorization="Bearer " + token),
                         content_type='application/json')
        response = self.client.get('/api/v2/party/1',
                                   headers=dict(Authorization="Bearer " + token),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)

    def test_get_wrong_political_party(self):
        token = self.get_token()
        self.client.get('/api/v2/party', data=self.add_party,
                        headers=dict(Authorization="Bearer " + token),
                        content_type='application/json')
        response = self.client.get('/api/v2/party/10',
                                   headers=dict(Authorization="Bearer " + token),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 404)

    def test_political_update_successfully(self):
        token = self.get_token()
        self.client.post('/api/v2/party', data=self.add_party,
                         headers=dict(Authorization="Bearer " + token),
                         content_type='application/json')
        response = self.client.patch('/api/v2/party/1/name', data=self.update_party,
                                     headers=dict(Authorization="Bearer " + token),
                                     content_type='application/json',
                                     )
        self.assertEqual(response.status_code, 200)

    def test_political_update_forbidden(self):
        token = self.get_token()
        response = self.client.patch('/api/v2/party/56/name', data=self.update_party,
                                     headers=dict(Authorization="Bearer " + token),
                                     content_type='application/json',
                                     )
        self.assertEqual(response.status_code, 404)

    def test_delete_non_existing_party(self):
        token = self.get_token()
        response = self.client.delete('/api/v2/party/e',
                                      headers=dict(Authorization="Bearer " + token),
                                      content_type='application/json',
                                      )
        self.assertEqual(response.status_code, 404)
