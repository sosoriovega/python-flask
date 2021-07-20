
import json

from tests.BaseCase import BaseCase

class TestUserLogin(BaseCase):

    def test_successful_login(self):
        # Given
        email = "sosoriov@gmail.com"
        password = "sergio77"
        user_payload = json.dumps({
            "email": email,
            "password": password
        })

        self.app.post('/create/users', headers={"Content-Type": "application/json"}, data=user_payload)
        response = self.app.post('/login/users', headers={"Content-Type": "application/json"}, data=user_payload)
        login_token = response.json['token']

        address_payload = {
            "postalcode": "12345",
            "municipality": "cuernavaca",
            "state": "morelos",
            "neighborhood": "nardo 10 satelite",
            "primary": "True"
        }
        # When
        response = self.app.post('/create/users/1/addresses',
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {login_token}"},
            data=json.dumps(address_payload))

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)