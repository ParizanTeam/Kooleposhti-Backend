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
from django.conf.urls import include
from django.urls import base, path
from .views import *
from rest_framework_nested import routers
from pprint import pprint
from django.urls import re_path
from rest_framework_simplejwt import views


router = routers.DefaultRouter()
router.register('', ImageViewSet, basename='images-images')


urlpatterns = [
    path('', include(router.urls)),
]
