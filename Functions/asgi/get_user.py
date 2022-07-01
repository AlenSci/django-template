from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(query_string):
    user_id = None
    token = parse_qs(query_string.decode("utf8")).get('token')
    if token:
        token = token[0]
    else:
        return 'please provide a token'
    instance = Token.objects.filter(key=token).first()
    if not instance:
        return None
    return instance.user
