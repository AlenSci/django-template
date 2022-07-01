from django.urls import path

from alerts.consumers.notification_consumer import AlertConsumer
from chat.consumer import ChatConsumer

websocket_urlpatterns = [
    path(r'alerts/', AlertConsumer.as_asgi()),
    path(r'chat/<int:pk>/', ChatConsumer.as_asgi()),
    # re_path(r'chat_monitor/(?P<chat_id>[^/]+)/$', MonitorConsumer.as_asgi()),
    # re_path(r'notifications_monitor/$', NotificationMonitorConsumer.as_asgi()),
    # re_path(r'notifications/$', NotificationConsumer.as_asgi()),
    # re_path(r'dashboard/$', DashBoardConsumer.as_asgi())
]
