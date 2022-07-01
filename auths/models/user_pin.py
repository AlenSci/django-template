from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from Functions.getChangedFields import get_changed_fields
from Functions.modles.BaseModel import BaseModel
from auths.functions.handle_pin_code import check_user_pin, create_user_pin
from users.models import User


class UserPin(BaseModel):
    CHOICES = (
        ('email verification', 'email verification'),
        ('password reset', 'password reset'),
    )

    type = models.CharField(blank=True, null=True, max_length=255, choices=CHOICES)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_pin')
    generated_number = models.IntegerField(default=0)
    trials_number = models.IntegerField(default=0)
    pin = models.IntegerField(blank=True, null=True)
    last_modified_at = models.DateTimeField(auto_now=True, editable=False)


class ModelSer(serializers.ModelSerializer):
    pin = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)

    class Meta:
        model = UserPin
        fields = ['pin', 'type', 'email']


class UserPinValidation(GenericAPIView):
    serializer_class = ModelSer
    permission_classes = (AllowAny,)
    allowed_methods = ['post']

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data.get('email')).first()
        res = check_user_pin(user, request.data.get('type'), request.data.get('pin'))

        if res is True:
            return Response(
                {"detail": _("Ok")}
            )
        return Response(
            res, status=status.HTTP_404_NOT_FOUND
        )


@receiver(post_save, sender=User)
def createUserPin(created, instance, **kwargs):
    if created:
        try:
            create_user_pin(instance, 'email verification')
        except:
            pass

@receiver(pre_save, sender=UserPin)
def send_email(instance, **kwargs):
    changes = get_changed_fields(UserPin, instance)
    if changes:
        pin = changes['new data'].get('pin')
        if pin:
            pass
            # from django.core.mail import send_mail
            # celeryApp.send_mail().delay()
            # send_mail(instance.type.title(),
            #           f"""Please use the following code as your {instance.type} Code: {instance.pin}""",
            #           settings.SENDER_EMAIL, [instance.user.email])
