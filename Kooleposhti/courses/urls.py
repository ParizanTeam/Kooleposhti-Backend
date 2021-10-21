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
from .views import CourseList, ReviewViweSet
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('', CourseList, basename=None)
courses_router = routers.NestedDefaultRouter(
    parent_router=router, parent_prefix='', lookup='course')  # course_pk
courses_router.register('reviews', ReviewViweSet, basename='course-reviews')
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
    # path('', CourseList.as_view()),
    # path('<int:pk>/', course_detail),
]
