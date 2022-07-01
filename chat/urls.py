from django.urls import path

from chat.models import ChatsView, ChatView

urlpatterns = [
    path('', ChatsView.as_view()),
    path('<int:pk>/', ChatView.as_view()),
]
