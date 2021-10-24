from django.urls import reverse
import rest_framework
from .models import User
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from accounts.models import Instructor, Student
from .serializers import InstructorSerializer, StudentSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import permissions
from rest_framework.test import APIRequestFactory
from accounts import serializers
# Create your views here.


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [
    #     IsAdminUser
    #     # DjangoModelPermission
    # ]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=IsAuthenticated)
    def me(self, request):
        student, is_created = Student.objects.get_or_create(pk=request.user.id)
        if request.method == 'GET':
            # Anonymous User : not logged in
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = StudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data


class InstructorList(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def get_serializer_context(self):
        return {
            'request': self.request
        }


@api_view(http_method_names=permissions.SAFE_METHODS)
def reset_user_password(request, *args, **kwargs):
    pass


@api_view(http_method_names=permissions.SAFE_METHODS)
def activate_user_account(request, *args, **kwargs):
    factory = APIRequestFactory()
    request = factory.post(
        path=reverse('user-activation'),
        data={
            'uid': kwargs.get('uid'),
            'token': kwargs.get('token')
        },
        format='json'
    )
    return Response(template_name="email/activation.html")


# accounts/activate/{uid}/{token}
