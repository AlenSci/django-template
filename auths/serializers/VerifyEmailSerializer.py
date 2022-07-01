from django.utils.translation import gettext_lazy as _
from rest_auth.registration.views import VerifyEmailView
from rest_framework import serializers, status
from rest_framework.response import Response

from auths.functions.handle_pin_code import create_user_pin, check_user_pin
from home.api.v1.serializers import UserSerializer
from users.models import User


class VerifyEmailSerializer(serializers.Serializer):
    pin = serializers.CharField(required=True)
    email = serializers.CharField(required=False)


class CustomVerifyEmailView(VerifyEmailView):
    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        pin = request.data.get('pin')
        try:
            pin = int(pin)
        except:
            pass
        query = {}

        if email: query['email'] = email

        try:
            u = User.objects.get(**query)
        except Exception as e:
            raise serializers.ValidationError(_(str(e)))
        if not pin:
            res = create_user_pin(u, 'email verification')
            if res is True: return Response('A new pin code has been sent to your email.', status=status.HTTP_200_OK)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        res = check_user_pin(u, 'email verification', pin)

        if res is True:
            u.is_email_verified = True
            u.save()
            return Response({
                'key': u.auth_token.key,
                'user': UserSerializer(u, many=False).data
            }, status=status.HTTP_200_OK)
        else:
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
