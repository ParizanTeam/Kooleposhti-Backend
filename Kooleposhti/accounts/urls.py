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
from .api import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import SimpleRouter
from pprint import pprint

router = SimpleRouter()
router.register('instructors', InstructorList)
# urlpatterns = router.urls


# pprint(router.urls)
urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
    path('', include(router.urls)),
    # path('students/', StudentViewSet.as_view),
    # path('instructors/<int:pk>/', InstructorList.as_view(),
    #      name='instructor-detail'),
    # path('instructors/', InstructorList.as_view(), name='all_instructors'),
]
