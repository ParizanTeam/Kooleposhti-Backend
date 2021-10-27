from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from accounts.models import Student, Instructor
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    # birth_date = serializers.DateField()
    is_instructor = serializers.BooleanField(default=False)

    class Meta ():
        model = settings.AUTH_USER_MODEL
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name',
                  'is_instructor'
                  #   'birth_date',
                  ]

    def create(self, validated_data):
        if 'is_instructor' in validated_data:
            del validated_data['is_instructor']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'is_instructor' in validated_data:
            del validated_data['is_instructor']
        return super().update(instance, validated_data)


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('birth_date',)


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
        ref_name = "My User Serializer"
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
