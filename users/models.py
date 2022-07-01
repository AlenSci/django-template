from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from safedelete.models import SafeDeleteModel

from Functions.views.MyViews import ItemsView, ItemView, convert_to_list


class User(SafeDeleteModel, AbstractUser):
    is_deleted = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    photo = models.ImageField(null=True, blank=True, upload_to='images/')

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def get_user_permissions(self):
        user_permissions = convert_to_list(self.user_permissions.all())
        for group in self.groups.all():
            groups_permissions = convert_to_list(group.permissions.all())
            user_permissions += list(groups_permissions)
        return user_permissions

    class Meta:
        get_latest_by = 'date_joined'


Model = User


class ModelSer(DynamicFieldsMixin, serializers.ModelSerializer):
    def to_representation(self, instance):
        return super().to_representation(instance)

    class Meta:
        model = Model
        fields = '__all__'


class PutModelSer(ModelSer):
    class Meta:
        model = Model
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': False},
            'username': {'required': False},
        }


class UsersView(ItemsView):
    serializer_class = ModelSer
    queryset = Model.objects.all()

    # def check_object_permissions(self, request, objs):
    #     pass


class UserView(ItemView):
    serializer_class = ModelSer
    queryset = Model.objects.all()

    def object_permissions(self, request, obj):
        return request.user.id == obj.id

    def put(self, request, pk):
        self.serializer_class = PutModelSer
        return super().put(request, pk)
