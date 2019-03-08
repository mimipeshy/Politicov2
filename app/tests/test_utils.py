# import json
# import unittest
#
# from app.tests.base_test import BaseTests
#
#
# class ValidationTests(BaseTests):
#     def test_empty_strings(self):
#         """Tests API can get all offices"""
#         token = self.get_token()
#         response = self.client.post('/api/v2/party', data=self.empty_party_name,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 400)
#
#     def test_empty_logo_string(self):
#         token = self.get_token()
#         response = self.client.post('/api/v2/party', data=self.empty_logoUrl,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 400)
#
#     def test_empty_hqaddress_string(self):
#         token = self.get_token()
#         response = self.client.post('/api/v2/party', data=self.empty_hqAddress,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 400)
#
#     def test_short_name_length(self):
#         token = self.get_token()
#         response = self.client.post('/api/v2/party', data=self.length_name,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 400)
#         response = self.client.post('/api/v2/party', data=self.length_hqAddress,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 400)
#         response = self.client.post('/api/v2/party', data=self.length_type,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 400)
#
#     def validate_logo(self):
#         token = self.get_token()
#         response = self.client.post('/api/v2/party', data=self.missing_http,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 403)
#         response = self.client.post('/api/v2/party', data=self.missing_body,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 403)
#         response = self.client.post('/api/v2/party', data=self.missing_path,
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 403)
#
#     def validate_strings(self):
#         token = self.get_token()
#         response = self.client.post('/api/v2/party', data=self.validate_strings(),
#                                     headers=dict(Authorization="Bearer " + token),
#                                     content_type='application/json')
#         self.assertEqual(response.status_code, 400)
#
#
# if __name__ == '__main__':
#     unittest.main()
