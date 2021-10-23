from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from accounts.models import Student, Instructor
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    # birth_date = serializers.DateField()

    class Meta (BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name',
                  #   'birth_date',
                  ]


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')


class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'user_id',
            'birth_date',
        ]


class UserSerializer(BaseUserSerializer):
    #  'current_user': 'djoser.serializers.UserSerializer',
    class Meta (BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
