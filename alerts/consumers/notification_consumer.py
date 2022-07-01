import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# from home.models import Alert
from alerts.models.alert import Alert, AlertSerializer


class AlertConsumer(WebsocketConsumer):
    def connect(self, *args, **kwargs):
        async_to_sync(self.channel_layer.group_add)(
            'notification_group',
            self.channel_name
        )
        self.accept()
        self.user = self.scope.get('user')
        if self.user is None: self.send('Invalid token.'); self.close()

    def receive(self, text=None, text_data=None, content=None, **kwargs):
        text_data = json.loads(text_data)
        id = int(text_data.get('id'))
        is_read = str(text_data.get('is_read')).lower() == 'true'
        if is_read:
            alert = Alert.objects.get(id=id)
            alert.is_read = True
            alert.save()
            data = {"status": 'true', 'message': f'alert with id {id} is read by user with id {self.user.id}'}
            self.send(json.dumps(data))

    def handle_notifications(self, event):
        # from backports import zoneinfo
        # from jonathan_kim_teenge_34184.settings import VIEW_TIMEZONE
        # from django.utils import timezone

        id = int(event.get('id'))
        if id:
            alert = Alert.objects.filter(id=id).first()
            if self.user == alert.user:
                # timezone.activate(zoneinfo.ZoneInfo(VIEW_TIMEZONE))
                alert = AlertSerializer(alert, many=False).data
                self.send(json.dumps(alert))
        else:
            print('no id')