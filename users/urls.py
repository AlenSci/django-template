from django.urls import path

from users.models import UsersView, UserView
from users.views import (
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

app_name = "users"
urlpatterns = [
    path('', UsersView.as_view()),
    path('<int:pk>/', UserView.as_view()),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
