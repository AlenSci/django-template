import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from icecream import ic

from chat.models import Message, Chat

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self, *args, **kwargs):
        self.user = self.scope['user']
        id = int(self.scope['url_route']['kwargs']['pk'])

        self.chat = Chat.objects.filter(id=id).first()
        self.accept()

        if self.user not in self.chat.users.all():
            self.send('You are not in this chat room.')
            self.close()
            return

        self.room_group_name = str(self.chat.id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data, **kwargs):
        c = json.loads(text_data)
        # 2. handle messages
        is_blocked = False
        if hasattr(self.user, 'channel_layer'):
            is_blocked = self.user.channel_layer.is_blocked
        if is_blocked:
            self.send(json.dumps({
                'error': 'You are blocked from sending messages.'
            }))
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'handle_messages',
                    'content': c['message'],
                    'sender': self.user.id
                }
            )
            Message.objects.create(content=c['message'], created_by=self.user, chat=self.chat)

    def handle_messages(self, event):
        content = event['content']
        sender = event.get('sender')
        data = {
            'message': content,
            'sender': sender,
        }
        if sender: sender = int(sender)
        if self.user.id != sender: self.send(json.dumps(data))

        # sender = User.objects.get(id=sender)
        # m = list(Message.objects.all().order_by('created_at'))
        #
        # # set message is read
        # try:
        #     m = m[-2]
        #
        #     if sender.id != m.created_by.id:
        #         m = Message.objects.filter(id=m.id).first()
        #         if m:
        #             m.is_read = True
        #             m.save()
        # except:
        #     pass
