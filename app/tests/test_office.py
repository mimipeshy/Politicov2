import json
import unittest

from app.tests.base_test import BaseTests



class PoliticalOfficeTests(BaseTests):
    """Tests functionality of the political office endpoint"""

    def test_create_an_office(self):
        # self.register_user(first_name="peris", last_name="ndanu", other_name="kimeu", email="perisndanu@gmail.com",
        #                    password="South@frica1", phone="1234567890", passportUrl="pic/jpg", is_admin=True)
        # data = self.login_user(email="perisndanu@gmail.com", password="South@frica1")
        # access_token = json.loads(data.data.decode())['token']
        response = self.client().post('/api/v2/office', data=self.add_office,
                                      content_type='application/json',
                                      # headers=access_token
                                      )
        self.assertEqual(response.status_code, 201)
#
#         response = self.client().post('/api/v2/office', data=self.add_office,
#                                       content_type='application/json',
#                                       headers=self.authHeaders
#                                       )
#         self.assertEqual(response.status_code, 404)
#
#     def test_get_all_offices(self):
#         """Tests API can get all offices"""
#         # access_token = self.user_token_get()
#         self.client().post('/api/v2/office', data=self.add_office,
#                            content_type='application/json',
#                            # headers=self.authHeaders
#                            )
#         response = self.client().get('/api/v2/office',
#                                      content_type='application/json',
#                                      # hheaders=self.authHeaders
#                                      )
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_specific_office_by_id(self):
#         """Tests API can get a specific party by using its id"""
#         # access_token = self.user_token_get()
#         self.client().post('/api/v2/office', data=self.add_office,
#                            content_type='application/json',
#                            # headers=self.authHeaders
#                            )
#         response = self.client().get('/api/v2/office/1',
#                                      content_type='application/json',
#                                      # headers=self.authHeaders
#                                      )
#         self.assertEqual(response.status_code, 200)
#
#     def test_get_office_forbidden(self):
#         # access_token = self.user_token_get()
#         self.client().post('/api/v2/office', data=self.add_office,
#                            content_type='application/json')
#         response = self.client().get('/api/v2/office/10',
#                                      content_type='application/json',
#                                      # headers=dict(Authorization="Bearer " + access_token)
#                                      )
#         self.assertEqual(response.status_code, 404)
#
#
# if __name__ == '__main__':
#     unittest.main()
