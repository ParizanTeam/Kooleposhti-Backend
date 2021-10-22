from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from accounts.models import Student, Instructor, User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_no = serializers.CharField(max_length=11, min_length=11)
    class Meta:
        model = User
        fields = ('id','username','password', 'email', 'first_name', 'last_name', 'phone_no')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):

        # user = self.Meta.model(**validated_data)
        user = User.objects.create_user(
            validated_data['username'],  
            email= validated_data['email'],
            password = validated_data['password'],
            first_name=validated_data['first_name'],  
            last_name=validated_data['last_name'],
            phone_no=validated_data['phone_no'],
            )
        password = validated_data.pop('password', None)
        if password is not None:
            user.set_password(password)
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class UserCreateSerializer(BaseUserCreateSerializer):
#     class Meta (BaseUserCreateSerializer.Meta):
#         fields = ['id', 'username', 'password',
#                   'password', 'email', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name']


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
