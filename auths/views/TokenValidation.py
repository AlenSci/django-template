from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class ModelSer(serializers.ModelSerializer):
    key = serializers.IntegerField(required=True)


class TokenValidation(GenericAPIView):
    serializer_class = ModelSer
    permission_classes = (AllowAny,)
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        token = Token.objects.filter(key=request.data.get('key')).first()
        if token:
            return Response(
                {"detail": _("Ok")}
            )
        return Response(
            {"detail": _("Invalid token")}, status=status.HTTP_404_NOT_FOUND
        )
