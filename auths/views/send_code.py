from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, mixins, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auths.models import UserPin, create_user_pin, User


class ModelSer(serializers.Serializer):
    email = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=UserPin.CHOICES)


class ResendCodePinView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["post"]
    serializer_class = ModelSer

    def post(self, request):
        """
        ### note: type can be 'email verification', 'password reset'
        """
        email = request.data.get('email')
        type_ = request.data.get('type')
        u = User.objects.filter(email=email).first()
        if u:
            res = create_user_pin(u, type_)
            if res is True:
                return Response(f'A new code pin has been sent to {email}')
            else:
                raise serializers.ValidationError(_(res))
        else:
            return Response('Not found.', status=status.HTTP_404_NOT_FOUND)
