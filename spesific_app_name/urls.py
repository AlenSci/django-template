from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from allauth.account.views import confirm_email
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls

from spesific_app_name import description
from spesific_app_name.settings import env

urlpatterns = [
    path("alerts/", include("alerts.urls")),
    path("chat/", include("chat.urls")),
    path("trash/", include("trash.urls")),
    path("rest-auth/", include("auths.urls")),
    path("", include("home.urls")),
    path("accounts/", include("allauth.urls")),
    path("modules/", include("modules.urls")),
    # path("api/v1/", include("home.api.v1.urls")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("rest-auth/", include("rest_auth.urls")),
    # Override email confirm to use allauth's HTML view instead of rest_auth's API view
]

admin.site.site_header = "Kakoufils"
admin.site.site_title = "Kakoufils Admin Portal"
admin.site.index_title = "Kakoufils Admin"

# swagger
api_info = openapi.Info(
    title="Ancient Frog API",
    default_version="v1",
    description="API documentation for Ancient Frog App",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns += [
    path('api-docs/',
         include_docs_urls(title=env.str("PROJECT_NAME", default='project name'), description=description.description)),
]

urlpatterns += [path("", TemplateView.as_view(template_name='index.html'))]
urlpatterns += [re_path(r"^(?:.*)/?$",
                        TemplateView.as_view(template_name='index.html'))]
