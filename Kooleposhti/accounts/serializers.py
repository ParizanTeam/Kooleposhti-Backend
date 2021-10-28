from rest_framework_simplejwt.serializers import PasswordField
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework.exceptions import ValidationError
from rest_framework import exceptions, serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from rest_framework import serializers
from accounts.models import Student, Instructor, User
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    # birth_date = serializers.DateField()
    is_instructor = serializers.BooleanField(default=False)
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password2"] = serializers.CharField(
            style={"input_type": "password"}
        )
        self.fields['is_instructor'] = serializers.BooleanField(
            default=False
        )

    def validate(self, attrs):
        self.fields.pop("password2", None)
        re_password = attrs.pop("password2")
        self.fields.pop('is_instructor')
        attrs.pop('is_instructor')
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")

    class Meta ():
        model = User
        fields = ['id', 'username', 'password',
                  'email',
                  #   'first_name', 'last_name',
                  'is_instructor',
                  #   'birth_date',
                  ]

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError("Passwords Do not match")
    #     return super().validate(attrs)

    # def create(self, validated_data):
    #     validated_data_cp = self.excluded_fields(validated_data)
    #     user = User.objects.create_user(**validated_data_cp)
    #     return user

    # def excluded_fields(self, validated_data):
    #     validated_data_cp = validated_data.copy()
    #     if 'is_instructor' in validated_data:
    #         del validated_data_cp['is_instructor']
    #     if 'password2' in validated_data:
    #         del validated_data_cp['password2']
    #     return validated_data_cp

    # def update(self, instance, validated_data):
    #     validated_data_cp = self.excluded_fields(validated_data)
    #     return super().update(instance, validated_data_cp)


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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer, serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(default=None)
        self.fields['password'] = PasswordField()
        self.fields['email'] = serializers.EmailField(default=None)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def super_validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
            'email': attrs['email'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    def validate(self, attrs):
        data = self.super_validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
