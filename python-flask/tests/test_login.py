import json

from tests.BaseCase import BaseCase

class TestUserLogin(BaseCase):

    def test_successful_login(self):
        # Given
        email = "sosoriov@gmail.com"
        password = "sergio123"
        payload = json.dumps({
            "email": email,
            "password": password
        })
        response = self.app.post('/create/users', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post('/login/users', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)