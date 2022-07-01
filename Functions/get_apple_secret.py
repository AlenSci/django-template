from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone


def get_apple_secret():
    headers = {
        'kid': settings.SOCIAL_AUTH_APPLE_ID_KEY
    }

    payload = {
        'iss': settings.SOCIAL_AUTH_APPLE_ID_TEAM,
        'iat': timezone.now(),
        'exp': timezone.now() + timedelta(days=180),
        'aud': 'https://appleid.apple.com',
        'sub': settings.SOCIAL_AUTH_APPLE_ID_CLIENT,
    }

    client_secret = jwt.encode(
        payload,
        settings.SOCIAL_AUTH_APPLE_PRIVATE_KEY,
        algorithm='ES256',
        headers=headers
    ).decode("utf-8")

    return client_secret