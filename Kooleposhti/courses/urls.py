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
from .views import *
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from pprint import pprint

app_name = 'courses'

router = routers.DefaultRouter()
router.register('courses', CourseViewSet, basename=None)
router.register('carts', ShoppingCartViewSet)
router.register('categories', CategoryViewSet)
# pprint(router.urls)

courses_router = routers.NestedDefaultRouter(
    parent_router=router, parent_prefix='courses', lookup='course')  # course_pk
courses_router.register('reviews', ReviewViweSet, basename='course-reviews')
courses_router.register('sessions', SessionViewSet, basename='course-sessions')


carts_router = routers.NestedDefaultRouter(
    parent_router=router, parent_prefix='carts', lookup='cart')
carts_router.register('items', ShoppingCartItemViewSet, basename='cart-items')
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
    path('', include(carts_router.urls)),
    # path('', CourseList.as_view()),
    # path('<int:pk>/', course_detail),
]
