from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from auths.functions.handle_pin_code import check_user_pin
from users.models import User


class PasswordConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    email = serializers.CharField()
    pin = serializers.CharField()

    # set_password_form_class = SetPasswordForm

    def validate(self, attrs):
        if attrs.get('new_password1') == attrs.get('new_password2'):
            self.new_password = attrs.get('new_password1')
        else:
            raise serializers.ValidationError(_('Password fields not matched'))

        try:
            self.user = User.objects.get(email=attrs.get('email'))
        except Exception as e:
            raise serializers.ValidationError(_(str(e)))

        res = check_user_pin(self.user, 'password reset', attrs.get('pin'))
        if res is True:
            return super().validate(attrs)

        raise serializers.ValidationError(_(res))

    def save(self):
        u = self.user
        u.set_password(self.new_password)
        u.save()
        return
