from faker import Faker
from icecream import ic
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from users.models import User

fake = Faker()


def makeUsers(self):
    # add client
    client = APIClient()
    self.client = client

    for i in range(1, 4):
        params = {'name': fake.name(),
                  'email': fake.email(),
                  'password': 'Password123',
                  'first_name': fake.name(),
                  'last_name': fake.name()}
        res = self.client.post('/rest-auth/signup/', params)

        u = User.objects.last()
        u.is_email_verified = True
        u.save()

        res = self.client.post('/rest-auth/login/', {'email': params['email'], 'password': 'Password123'})

        setattr(self, f'token_{i}', res.data['key'])
        setattr(self, f'user_{i}', User.objects.last())
    user = self.user_1
    user.is_superuser = True
    user.save()

    client.credentials(HTTP_AUTHORIZATION=f'Token {self.token_1}')
    self.client = client


class TestClass(APITestCase):

    def printJ(self, d):
        from pygments import highlight
        from pygments.lexers.web import JsonLexer
        from pygments.formatters.terminal256 import Terminal256Formatter
        from pygments.style import Style
        from pygments.token import Token

        import json

        class MyStyle(Style):
            styles = {
                Token.String: 'ansibrightgreen ansibrightgreen',
                Token.Number: 'ansiwhite ansired',
                Token.Generic: 'ansiwhite ansibrightred',
                Token.Punctuation: 'ansiwhite ansiyellow',
                Token.Keyword: 'ansiwhite ansibrightred',
                Token.Literal: 'ansiwhite ansibrightred',
                Token.Literal.Number: 'ansiblue ansibrightred',
                Token.Operator: 'ansiwhite ansiwhite',
                Token.Other: 'ansibrightblue ansibrightblue',
            }

        try:
            d = json.dumps(d, indent=10, default=str)
        except:
            d = str(d)

        print(highlight(
            d,
            lexer=JsonLexer(),
            formatter=Terminal256Formatter(style=MyStyle), ))

    def setUp(self):
        self.fake = Faker()
        makeUsers(self)

    def login_as(self, user=None):
        if user:
            # self.client.post("/rest-auth/logout/")
            res = self.client.post("/rest-auth/login/", {'email': user.email, 'password': 'Password123'})
            client = APIClient()
            client.credentials(HTTP_AUTHORIZATION=f'Token {res.data["key"]}')
            self.client = client
        else:
            self.client = APIClient()

    def test(self):
        assert self.user_2.username
