import json
import unittest

from app.tests.base_test import BaseTests


class ValidationTests(BaseTests):
    def test_empty_strings(self):
        """Tests API can get all offices"""

        response = self.client().post('/api/v2/party', data=self.empty_party_name,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_empty_logo_string(self):
        response = self.client().post('/api/v2/party', data=self.empty_logoUrl,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_empty_hqaddress_string(self):
        response = self.client().post('/api/v2/party', data=self.empty_hqAddress,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_short_name_length(self):
        response = self.client().post('/api/v2/party', data=self.length_name,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client().post('/api/v2/party', data=self.length_hqAddress,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response = self.client().post('/api/v2/party', data=self.length_type,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def validate_logo(self):
        response = self.client().post('/api/v2/party', data=self.missing_http,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response = self.client().post('/api/v2/party', data=self.missing_body,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response = self.client().post('/api/v2/party', data=self.missing_path,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 403)
    def validate_strings(self):
        response = self.client().post('/api/v2/party', data=self.validate_strings(),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
