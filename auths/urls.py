from allauth.account.views import confirm_email
from django.conf.urls import url
from django.urls import path, include
from dotenv import load_dotenv
from rest_auth.registration.views import RegisterView
from rest_auth.views import (
    LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView, LoginView
)
from rest_framework.routers import DefaultRouter

from auths.models.user_pin import UserPinValidation
from auths.views.TokenValidation import TokenValidation
from auths.views.send_code import ResendCodePinView
from auths.views.verify_email import CustomVerifyEmailView

load_dotenv(verbose=True)
router = DefaultRouter()

urlpatterns = [
    path('request_pin_code/', ResendCodePinView.as_view()),
    path("signup/account-confirm-email/<str:key>/", confirm_email),
    # path("signup/", include("rest_auth.registration.urls")),
    path("", include(router.urls)),
    url(r'^password/reset/$', PasswordResetView.as_view(),name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
    url(r'^password/change/$', PasswordChangeView.as_view(),
        name='rest_password_change'),

    # path("signup/", include("rest_auth.registration.urls")),
    # path("signup/", SignupViewSet.as_view(), name="signup"),
    path("signup/", RegisterView.as_view(), name="signup"),

    path("verify-email/", CustomVerifyEmailView.as_view()),
    # path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    url(r'^token_validation/$', TokenValidation.as_view(), name='token_validation'),
    url(r'^pin_validation/$', UserPinValidation.as_view(), name='pin_validation'),
    # URLs that require a user to be logged in with a valid session / token.
    # path("rest-auth/registration/", include("rest_auth.registration.urls")),
]
