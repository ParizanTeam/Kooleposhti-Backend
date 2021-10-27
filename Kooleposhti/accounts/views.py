from .serializers import UserCreateSerializer
# from . signals import user_created
from validate_email import validate_email
from django.http.request import HttpRequest
from django.urls import reverse
import rest_framework
from .models import User, Verification
from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from accounts.models import Instructor, Student
from .serializers import InstructorSerializer, StudentSerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import permissions, status
from rest_framework.test import APIRequestFactory
from accounts import serializers
from rest_framework.test import RequestsClient
from django.conf import settings
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
    # accounts/activate/{uid}/{token}
    client = RequestsClient()
    response = client.post(
        url=f"{settings.WEBSITE_URL}{reverse('user-activation')}",
        data={
            'uid': kwargs.get('uid'),
            'token': kwargs.get('token')
        }
    )
    return render(request=request, template_name="email/activation.html")


@api_view(http_method_names=['POST'])
def check_email(request):
    try:
        User.objects.get(email=request.data['email'])
        return Response(f"email '{request.data['email']}' already exists!",
                        status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response(status=status.HTTP_200_OK, data='New Email')


@api_view(http_method_names=['POST'])
def check_username(request):
    try:
        User.objects.get(username=request.data['username'])
        return Response(f"username '{request.data['username']}' is already taken!",
                        status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response(status=status.HTTP_200_OK, data='New Username')


@api_view(http_method_names=['POST'])
def check_code(request: HttpRequest, *args, **kwargs):
    email = request.data.get('email')
    token = request.data.get('token')
    if email is None:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Email is not Provided')
    if token is None:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Token is not Provided')
    if not token.isnumeric():
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='Token is in the wrong format')
    if not validate_email(email):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='email is in the wrong format')
    try:
        verification_obj = Verification.objects.get(email=email)
        if token != verification_obj.token:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='wrong or expired token')
    except Verification.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data='wrong email or expired token')
    return Response(data='Valid Email and Token', status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['POST'])
def sign_up_user(request: HttpRequest, *args, **kwargs):
    serializer = UserCreateSerializer(**request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
    is_instructor = serializer.data['is_instructor']
    user = serializer.save()
    if is_instructor:
        Instructor.objects.create(user=user)
    else:
        Student.objects.create(user=user)
