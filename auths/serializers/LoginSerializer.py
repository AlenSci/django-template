from django.utils.translation import gettext_lazy as _
# from django_restql.mixins import DynamicFieldsMixin
from rest_auth.app_settings import serializers
from rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from users.models import User


class LoginSer(LoginSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')

        username = attrs.get('username')

        if username:
            u = User.objects.filter(username=username).first()
        else:
            u = User.objects.filter(email=email).first()

        if email:
            attrs['username'] = u.username if u else '........'

        if u and not u.is_email_verified:
            raise serializers.ValidationError(_("Please verify your email address."))

        return super().validate(attrs)
