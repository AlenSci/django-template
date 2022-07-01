from asgiref.sync import async_to_sync
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_restql.mixins import DynamicFieldsMixin
from icecream import ic
from rest_framework import serializers, status
from rest_framework.response import Response

from Functions.modles.get_relational_obj import get_relational
from Functions.views.MyViews import ItemsView, ItemView, decode_image_field
from users.models import User


class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    is_read = models.BooleanField(default=False)


class AlertSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


@receiver(post_save, sender=Alert)
def make_new_notification(created, *args, **kwargs):
    import channels.layers
    instance = kwargs.get('instance')
    if created:
        layer = channels.layers.get_channel_layer()
        data = {'type': 'handle_notifications', 'id': instance.id, }
        async_to_sync(layer.group_send)('notification_group', data)


class AlertsView(ItemsView):
    serializer_class = AlertSerializer
    queryset = Alert.objects.all()

    def handle_data(self, data):
        data = super().handle_data(data)
        # data['user'] = data['user'][0]
        return super().handle_data(data)


class AlertView(ItemView):
    serializer_class = AlertSerializer
    queryset = Alert.objects.all()

    def object_permissions(self, request, obj):
        return request.user.id == obj.user.id
