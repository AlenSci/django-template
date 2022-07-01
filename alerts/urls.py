from django.urls import path

from alerts.models import AlertsView, AlertView

urlpatterns = [
    path('', AlertsView.as_view()),
    path('<int:pk>/', AlertView.as_view()),
]
