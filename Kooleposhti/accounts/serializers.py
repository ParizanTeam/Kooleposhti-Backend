from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from accounts.models import Student, Instructor, User
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    # birth_date = serializers.DateField()
    is_instructor = serializers.BooleanField(default=False)
    password1 = serializers.CharField(
        max_length=255, write_only=True, source='password')
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta ():
        model = User
        fields = ['id', 'username', 'password1', 'password2',
                  'email',
                  #   'first_name', 'last_name',
                  'is_instructor',
                  #   'birth_date',
                  ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords Do not match")
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data_cp = self.excluded_fields(validated_data)
        return super().create(validated_data_cp)

    def excluded_fields(self, validated_data):
        validated_data_cp = validated_data.copy()
        if 'is_instructor' in validated_data:
            del validated_data_cp['is_instructor']
        if 'password2' in validated_data:
            del validated_data_cp['password2']
        return validated_data_cp

    def update(self, instance, validated_data):
        validated_data_cp = self.excluded_fields(validated_data)
        return super().update(instance, validated_data_cp)


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
