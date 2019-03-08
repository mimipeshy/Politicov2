import json

from app.tests.base_test import BaseTests


class VoteTests(BaseTests):
    """"Tests functionality of the votes endpoint"""

    def test_vote_non_existing_candidate(self):
        token = self.get_token()
        response = self.client.post('/api/v2/votes', data=json.dumps({
                                                    "office": 1,
                                                    "candidate": 2,
                                                    "voter": 1

        }),headers=dict(Authorization="Bearer " + token),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
