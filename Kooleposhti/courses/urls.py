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
from .api.views import *
from .api.course import *
from .api.assignment import *
from .api.comment import *
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from pprint import pprint
from .api.discount import DiscountViewSet
app_name = 'courses'

router = routers.DefaultRouter()
router.register('courses', CourseViewSet, basename=None)
router.register('carts', ShoppingCartViewSet)
router.register('categories', CategoryViewSet)
router.register('assignments', AssignmentViewSet)
router.register('discounts', DiscountViewSet)

# pprint(router.urls)

courses_router = routers.NestedDefaultRouter(
    parent_router=router, parent_prefix='courses', lookup='course')  # course_pk
courses_router.register('reviews', ReviewViweSet, basename='course-reviews')
courses_router.register('sessions', SessionViewSet, basename='course-sessions')
courses_router.register('comments', CommentViewSet, basename='course-comments')

comments_router = routers.NestedDefaultRouter(
    parent_router=courses_router, parent_prefix='comments', lookup='parent')  # comment_pk
comments_router.register('reply', ReplytViewSet, basename='reply')

assignments_router = routers.NestedDefaultRouter(
    parent_router=router, parent_prefix='assignments', lookup='assignment')  # assignment_pk
assignments_router.register('submit', HomeworkViewSet, basename='homeworks')

homework_router = routers.NestedDefaultRouter(
    parent_router=assignments_router, parent_prefix='submit', lookup='homework')  # homework_pk
homework_router.register('feedback', FeedbackViewSet, basename='feedback')

carts_router = routers.NestedDefaultRouter(
    parent_router=router, parent_prefix='carts', lookup='cart')
carts_router.register('items', ShoppingCartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
    path('', include(carts_router.urls)),
    path('', include(assignments_router.urls)),
    path('', include(homework_router.urls)),
    path('', include(comments_router.urls)),
]
