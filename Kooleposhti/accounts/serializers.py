from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from accounts.models import Student, Instructor


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta (BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'password', 'email', 'first_name', 'last_name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name']


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
