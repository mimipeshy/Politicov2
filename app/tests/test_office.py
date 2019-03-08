from app.tests.base_test import BaseTests


class PoliticalOfficeTests(BaseTests):
    """Tests functionality of the political office endpoint"""

    def test_create_an_office(self):
        token = self.get_token()
        response = self.client.post('/api/v2/office', data=self.add_office,
                                    headers=dict(Authorization="Bearer " + token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_specific_office_by_id(self):
        """Tests API can get a specific party by using its id"""
        token = self.get_token()
        self.client.post('/api/v2/office', data=self.add_office,
                         headers=dict(Authorization="Bearer " + token),
                         content_type='application/json')
        response = self.client.get('/api/v2/office/1',
                                   headers=dict(Authorization="Bearer " + token),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)

    def test_get_office_forbidden(self):
        token = self.get_token()
        self.client.post('/api/v2/office', data=self.add_office,
                         headers=dict(Authorization="Bearer " + token),
                         content_type='application/json')
        response = self.client.get('/api/v2/office/10',
                                   headers=dict(Authorization="Bearer " + token),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 404)

    def test_get_all_offices(self):
        """Tests API can get all offices"""
        token = self.get_token()
        self.client.post('/api/v2/office', data=self.add_office,
                         headers=dict(Authorization="Bearer " + token),
                         content_type='application/json')
        response = self.client.get('/api/v2/office',
                                   headers=dict(Authorization="Bearer " + token),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
