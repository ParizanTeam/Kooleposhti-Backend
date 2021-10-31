from .serializers import MySendEmailResetSerializer, UserSerializer
from .email import PasswordChangedConfirmationEmail
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from .email import PasswordResetEmail
from djoser.serializers import PasswordResetConfirmRetypeSerializer
from djoser.serializers import SendEmailResetSerializer
from djoser.compat import get_user_email
from django.utils.timezone import now
from rest_framework_simplejwt.views import TokenViewBase
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
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import permissions, status
from rest_framework.test import APIRequestFactory
from accounts import serializers
from rest_framework.test import RequestsClient
from django import conf
from pprint import pprint
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
        s = Student.objects.first()
        pprint(dir(s))
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
        url=f"{conf.settings.WEBSITE_URL}{reverse('user-activation')}",
        data={
            'uid': kwargs.get('uid'),
            'token': kwargs.get('token')
        }
    )
    return render(request=request, template_name="email/activation.html")


@api_view(http_method_names=['POST', *SAFE_METHODS])
def check_email(request):
    if request.method == 'POST':
        try:
            User.objects.get(email=request.data['email'])
            return Response(f"email '{request.data['email']}' already exists!",
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK, data='New Email')


@api_view(http_method_names=['POST', *SAFE_METHODS])
def check_username(request):
    if request.method == 'POST':
        try:
            User.objects.get(username=request.data['username'])
            return Response(f"username '{request.data['username']}' is already taken!",
                            status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK, data='New Username')


@api_view(http_method_names=['POST', *SAFE_METHODS])
def check_code(request: HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        email = request.data.get('email')
        token = request.data.get('token')
        try:
            User.objects.get(email=email)
            try:
                verification_obj = Verification.objects.get(pk=email)
                verification_obj.delete()
            except Verification.DoesNotExist:
                pass
            return Response(status=status.HTTP_400_BAD_REQUEST, data='User is currently activated')
        except User.DoesNotExist:
            pass
        if email is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Email is not Provided')
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Token is not Provided')
        if not token.isnumeric():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='Token is in the wrong format')
        if not validate_email(email):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='email is in the wrong format')
        try:
            verification_obj = Verification.objects.get(pk=email)
            if token != verification_obj.token:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='wrong or expired token')
        except Verification.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='wrong email or expired token')
        verification_obj.delete()
        return Response(data='Valid Email and Token', status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['POST', *SAFE_METHODS])
def sign_up_user(request: HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        serializer_dict = {
            'username': request.data.get('username'),
            'password': request.data.get('password1'),
            'password2': request.data.get('password2'),
            'email': request.data.get('email'),
            # 'first_name': request.data.get('first_name'),
            # 'last_name': request.data.get('last_name'),
            'is_instructor': request.data.get('is_instructor', False),
        }
        is_instructor = serializer_dict.get('is_instructor')
        serializer = UserCreateSerializer(data=serializer_dict)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if is_instructor:
            Instructor.objects.create(user=user)
        else:
            Student.objects.create(user=user)
        # data = serializer.validated_data.copy()
        # del data['password']
        # del data['password2']
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND, data='Maybe your request method is not correct')


class MyTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = serializers.MyTokenObtainPairSerializer


class UserResetPassword(GenericViewSet):
    token_generator = default_token_generator
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'reset_password':
            return MySendEmailResetSerializer
        elif self.action == 'reset_password_confirm':
            return PasswordResetConfirmRetypeSerializer

        return UserSerializer

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        '''
        {
            "email": "mahdijavid1380@yahoo.com"
        }
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            PasswordResetEmail(request, context).send(to)

        return Response(status=status.HTTP_202_ACCEPTED, data={
            'url': conf.settings.PASSWORD_RESET_CONFIRM_URL.format(
                        uid=utils.encode_uid(user.pk),
                        token=default_token_generator.make_token(user)),
        })

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        '''
        {
            "uid": "",
            "token": "",
            "new_password": "",
            "re_new_password": ""
        }
        '''
        # serializer = PasswordResetConfirmRetypeSerializer(data=request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        context = {"user": serializer.user}
        to = [get_user_email(serializer.user)]
        PasswordChangedConfirmationEmail(request, context).send(to)
        return Response(status=status.HTTP_200_OK, data='password has been changed!')
