from django.urls import path, re_path

from trash.views import archive

urlpatterns = [
    path('', archive.Views.as_view(), name='trash'),
    path('<slug:app_label>/<slug:model>/<int:pk>/', archive.View.as_view(), name='trash'),
]
