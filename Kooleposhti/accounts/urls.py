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
from django.contrib import admin
from django.urls import path
from .views import *
from .email import ActivationEmail
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from pprint import pprint
from django.urls import re_path
from rest_framework_simplejwt import views


router = routers.DefaultRouter()
router.register('instructors', InstructorList)
router.register('students', StudentViewSet)
router.register('users', UserResetPassword, basename='user')
# urlpatterns = router.urls


# pprint(router.urls)
urlpatterns = [
    path('', include(router.urls)),
    path('password/reset/confirm/{uid}/{token}', reset_user_password),
    path('activate/', ActivationEmail.as_view(), name='activate'),
    path('checkemail/', check_email, name="check_email"),
    path('checkusername/', check_username, name="check-username"),
    path('signup/', sign_up_user, name='signup'),
    path('checkcode/', check_code, name='check_code'),
    re_path(r"^jwt/create/?", MyTokenObtainPairView.as_view(),
            name="jwt-create"),
    re_path(r"^jwt/refresh/?", views.TokenRefreshView.as_view(),
            name="jwt-refresh"),
    re_path(r"^jwt/verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
    # path('reset_password/', reset_password, name='reset_password'),
    # path('reset_password_confirm/', reset_password_confirm,
    #      name='reset_password_confirm'),
    # path('activate/<uid>/<token>', activate_user_account),
    # path('students/', StudentViewSet.as_view),
    # path('instructors/<int:pk>/', InstructorList.as_view(),
    #      name='instructor-detail'),
    # path('instructors/', InstructorList.as_view(), name='all_instructors'),
]
