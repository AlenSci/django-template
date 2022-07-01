# TODO move this to auths app
# class TokenSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(source='key')
#     profile = ProfileSerializer(source='user')
#
#     class Meta:
#         model = Token
#         fields = ('token', 'profile')


# class PasswordSerializer(PasswordResetSerializer):
#     """Custom serializer for rest_auth to solve reset password error"""
#     password_reset_form_class = ResetPasswordForm



# class ForgetPasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PasswordReset
#         fields = ('token',)