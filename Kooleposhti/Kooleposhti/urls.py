"""Kooleposhti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
# from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from marshmallow.utils import pprint
from rest_framework import permissions
from django.conf import settings


schema_view = get_schema_view(  # swagger/redoc
    openapi.Info(
        title="Kooleposhti",
        default_version="v1",
        description="Kooleposhti BackEnd",
        terms_of_service="Use it for good :)",
        contact=openapi.Contact(email=settings.EMAIL_HOST_USER),
        license=openapi.License(name="Kooleposhti License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('', include('courses.urls'), name='courses'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('swagger/', schema_view.with_ui('swagger',
                                         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
]

pprint(urlpatterns)

'''    
    path('openapi', get_schema_view(
            title="Blog API",
            description="A sample API for learning DRF",
            version="1.0.0"),
            name='openapi-schema'),
'''
