import datetime

from django.utils import timezone
from icecream import ic
from rest_framework.test import APIClient

from Functions.tests.mock_time import mock_time
from Functions.tests.test_class import TestClass
from auths.functions.handle_pin_code import create_user_pin
from auths.models.user_pin import UserPin
from users.models import User


class TestBasics(TestClass):

    def setUp(self):
        super().setUp()
        perams = {
            'email': 'ali@sci.com',
            'password': 'Password123',
        }
        self.perams = perams
        res = self.client.post('/rest-auth/signup/', perams)
        assert res.status_code == 201
        self.client = APIClient()

    def test(self):
        self.login_as(None)

        params = {'pin': 123456, "type": "password reset", "email": self.user_1.email, }
        res = self.client.post('/rest-auth/pin_validation/', params)
        assert "has no password reset pin code" in str(res.data)

        create_user_pin(self.user_1, "password reset")
        res = self.client.post('/rest-auth/pin_validation/', params)
        assert "Invalid code" in str(res.data)

        # # # --------------------------------------------------------
        pin = UserPin.objects.filter(user=self.user_1).last().pin
        params['pin'] = pin
        res = self.client.post('/rest-auth/pin_validation/', params)
        assert "Ok" in str(res.data)

    def test_invalid_pin_code(self):
        perams = {
            'pin': 123456,
            'email': 'ali@sci.com',
        }
        res = self.client.post('/rest-auth/verify-email/', perams)
        assert 'Invalid code.' in str(res.data)
        assert res.status_code == 400

    def test_request_new_code(self):
        perams = {
            'email': 'ali@sci.com',
        }
        u = User.objects.get(email='ali@sci.com')
        pin = UserPin.objects.get(user=u).pin
        res = self.client.post('/rest-auth/verify-email/', perams)
        assert pin != UserPin.objects.get(user=u).pin

    def test_too_many_request_new_code(self):
        perams = {
            'email': 'ali@sci.com',
        }
        for i in range(3):
            res = self.client.post('/rest-auth/verify-email/', perams)
        res = self.client.post('/rest-auth/verify-email/', perams)
        # ic(res.data)
        # ic(res.status_code)
        assert res.status_code == 400

        with mock_time(timezone.now() + datetime.timedelta(minutes=6)):
            res = self.client.post('/rest-auth/verify-email/', perams)
            assert res.status_code == 200
            # ic(res.data)

    def test_too_many_trials(self):
        perams = {
            'pin': 123456,
            'email': 'ali@sci.com',
        }
        for i in range(3):
            res = self.client.post('/rest-auth/verify-email/', perams)
            assert 'Invalid code' in str(res.data)
            assert res.status_code == 400

        res = self.client.post('/rest-auth/verify-email/', perams)
        assert res.status_code == 400
        assert 'You reached maximum' in str(res.data)

        with mock_time(timezone.now() + datetime.timedelta(minutes=6)):
            res = self.client.post('/rest-auth/verify-email/', perams)
            assert 'A new pin code' in str(res.data)

    def test_valid_pin_code(self):
        initial = UserPin.objects.count()
        u = User.objects.get(email='ali@sci.com')
        pin = UserPin.objects.get(user=u, type='email verification').pin
        perams = {
            'pin': str(pin),
            'email': 'ali@sci.com',
        }
        res = self.client.post('/rest-auth/login/', self.perams)
        assert res.status_code == 400

        assert not User.objects.get(email='ali@sci.com').is_email_verified
        res = self.client.post('/rest-auth/verify-email/', perams)
        assert res.data['key']
        assert res.status_code == 200
        assert UserPin.objects.count() == initial - 1
        assert User.objects.get(email='ali@sci.com').is_email_verified

        res = self.client.post('/rest-auth/login/', self.perams)
        assert res.status_code == 200

    def test_rest_password(self):
        self.login_as(None)

        count = User.objects.count()
        perams = {
            'email': self.user_1.email,
            'type': 'password reset',
        }
        self.perams = perams
        pins = UserPin.objects.filter(user=self.user_1)
        old_pin = pins[0].pin
        res = self.client.post('/rest-auth/request_pin_code/', perams)
        assert 'A new code pin has been sent to' in str(res.data)
        pins = UserPin.objects.filter(user=self.user_1, type='password reset')
        new_pin = pins[0].pin

        type_ = pins[0].type
        assert new_pin != old_pin

        perams = {"new_password1": "newpass", "new_password2": "newpass", "email": self.user_1.email, "pin": new_pin}
        res = self.client.post('/rest-auth/password/reset/confirm/', perams)
        assert 'Password has been reset with the new password.' in str(res.data)

    def test_rest_password_login(self):
        self.login_as(None)
        perams = {
            'email': self.user_1.email,
            'type': 'password reset',
        }
        res = self.client.post('/rest-auth/request_pin_code/', perams)

        pins = UserPin.objects.filter(user=self.user_1, type='password reset')
        perams = {"new_password1": "newpass", "new_password2": "newpass", "email": self.user_1.email,
                  "pin": pins[0].pin}

        params = {
            'email': self.user_1.email,
            'password': 'Password123',
        }
        res = self.client.post('/rest-auth/login/', params)
        assert res.status_code == 200

        res = self.client.post('/rest-auth/password/reset/confirm/', perams)
        assert 'Password has been reset with the new password.' in str(res.data)

        params = {
            'email': self.user_1.email,
            'password': 'Password123',
        }
        res = self.client.post('/rest-auth/login/', params)
        assert res.status_code == 400

        params['password'] = 'newpass'
        res = self.client.post('/rest-auth/login/', params)
        assert res.status_code == 200
