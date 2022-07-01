import os

from spesific_app_name.routings import websocket_urlpatterns
from spesific_app_name.settings import PROJECT_NAME

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frosty_breeze_25125.settings')
import django

django.setup()

from urllib.parse import parse_qs

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')


class QueryAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        from Functions.asgi.get_user import get_user

        scope['user'] = await get_user(scope["query_string"])

        queries = scope['query_string']
        queries = parse_qs(queries.decode("utf8"))
        for i in queries.keys():
            queries[i] = queries[i][0]

        for key, item in queries.items():
            import ast
            try:
                queries[key] = ast.literal_eval(item)
            except:
                pass
        scope['queries'] = queries
        return await self.app(scope, receive, send)


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": QueryAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
