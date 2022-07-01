from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

from Functions.modles.BaseModel import BaseModel
from Functions.views.MyViews import ItemsView, ItemView
from users.models import User


class Chat(BaseModel):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'A', _('Active')
        PASSIVE = 'P', _('Passive')

    users = models.ManyToManyField(User)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='chat_you_created', null=True,
                                   blank=True)

    def is_read(self):
        return not self.messages.filter(is_read=False).exists()
    #
    # def delete(self, using=None, keep_parents=False):
    #     self.is_deleted = True
    #     self.save(update_fields=['is_deleted'])
    #     self.messages.update(is_deleted=True)
    #     return 1


class Message(BaseModel):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'A', _('Active')
        PASSIVE = 'P', _('Passive')

    chat = models.ForeignKey('chat.Chat', on_delete=models.CASCADE,
                             related_name='messages')
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                   related_name='messages')
    content = models.TextField()
    status = models.CharField(choices=StatusChoices.choices, max_length=1,
                              default=StatusChoices.ACTIVE)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
        get_latest_by = 'created_at'


class ChatSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class ChatsView(ItemsView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class ChatView(ItemView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    # def object_permissions(self, request, obj):
    #     return request.user.id == obj.user.id
