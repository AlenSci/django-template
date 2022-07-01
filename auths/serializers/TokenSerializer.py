from django_restql.mixins import DynamicFieldsMixin
from rest_auth.models import TokenModel
from rest_auth.serializers import TokenSerializer

# from users.Views import user_views


class TokenSer(DynamicFieldsMixin, TokenSerializer):
    # user = user_views.ModelSer()

    class Meta:
        model = TokenModel
        fields = '__all__'
