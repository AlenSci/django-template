from icecream import ic
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from Functions.tests.test_class import TestClass


class TestBasics(TestClass):
    def test_get_current_user(self):
        res = self.client.get("/rest-auth/user/")
        assert res.data['pk'] == self.user_1.id

    def test_login(self):
        params = {
            'email': self.user_2.email,
            'password': 'Password123'
        }
        res = self.client.post('/rest-auth/login/', params)
        assert res.status_code == 200
        assert res.data['key']

    def test_logout_generate_new_token(self):
        params = {
            'email': self.user_1.email,
            'password': 'Password123'
        }
        res = self.client.post("/rest-auth/login/", params)
        token = res.data['key']
        self.client.post("/rest-auth/logout/")
        client = APIClient()
        res = client.post("/rest-auth/login/", params)
        assert token != res.data['key']

    def test_toke_validation(self):
        params = {
            'key': ''
        }
        res = self.client.post("/rest-auth/token_validation/", params)
        assert 404 == res.status_code

        params = {
            'key': Token.objects.last().key
        }
        res = self.client.post("/rest-auth/token_validation/", params)
        assert 200 == res.status_code
