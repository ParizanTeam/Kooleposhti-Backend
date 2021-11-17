from django.core.files.storage import Storage, default_storage
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.utils import model_meta
from rest_framework.response import Response
from images.models import MyImage
from images.serializers import ProfileImageSerializer
from .models import User
from rest_framework import serializers
from .serializers import update_relation
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.core.files.uploadedfile import InMemoryUploadedFile


class BaseUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    password = serializers.CharField(
        write_only=True, max_length=128, required=False)
    first_name = serializers.CharField(
        source='user.first_name', required=False, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(
        source='user.last_name', required=False, allow_blank=True, allow_null=True)
    phone_no = serializers.CharField(
        source='user.phone_no', required=False, max_length=11, allow_null=True, min_length=11)
    birth_date = serializers.DateField(
        source='user.birth_date', required=False, allow_null=True)
    roles = serializers.ReadOnlyField(
        source='user.get_user_roles', required=False, read_only=True)
    image = ProfileImageSerializer(
        source='user.image', required=False, allow_null=True)
    color = serializers.CharField(
        source='user.color', required=False, allow_null=True)
    image_url = serializers.URLField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        ref_name = None
        fields = ['id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'phone_no', 'birth_date',
                  'roles', 'image', 'color', 'image_url']

    def validate(self, attrs):
        if 'user' in attrs:
            phone_no = attrs['user'].get('phone_no', None)
            if phone_no:  # not None
                if not phone_no.isdigit():
                    raise serializers.ValidationError(
                        detail='phone number is not in the correct format', code='phone_no')
        return super().validate(attrs)

    def set_password(self, instance, validated_data):
        if not 'password' in validated_data:
            return
        password = validated_data.pop('password')
        try:
            validate_password(password, instance.user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )
        instance.user.set_password(password)
        instance.user.save()
        instance.save()

    def set_image(self, instance, validated_data, image_url=None):
        if not 'image' in validated_data:
            return
        image = validated_data.pop('image')
        print(type(image))
        # MyImage.objects.get(image=)
        if not 'image' in image and image_url is None:
            return
        # if isinstance(image['image'], InMemoryUploadedFile) :
        # if isinstance(image['image'], str):
        if not image_url is None:
            image_url = image_url.split(default_storage.base_url)[1]
            tmp_image = MyImage.get_image_id(image_url)
            if tmp_image is None:
                raise serializers.ValidationError(
                    detail='image url is not correct', code='image_url')
            image['image'] = tmp_image
        image = ProfileImageSerializer(data=image)
        image.is_valid(raise_exception=True)
        image = image.save()
        instance.user.image = image
        instance.save()

    def unique_constraint(self, validated_data, field):
        if not field in validated_data:
            return
        if User.objects.filter(**{field: validated_data[field]}).count() < 2:
            return
        self.fail(f'{field} exists')

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            if 'image' in validated_data['user']:
                self.set_image(
                    instance, validated_data['user'], validated_data.get('image_url'))
            update_relation(instance, validated_data, 'user')
        self.set_password(instance, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        # m2m_fields = []
        # for attr, value in validated_data.items():
        #     if attr in info.relations and info.relations[attr].to_many:
        #         m2m_fields.append((attr, value))
        #     else:
        #         setattr(instance, attr, value)
        self.context.get('request').user = instance.user
        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        # for attr, value in m2m_fields:
        #     field = getattr(instance, attr)
        #     field.set(value)
        return instance


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, required=False)
    # email = serializers.EmailField(read_only=True, required=False)
    # first_name = serializers.CharField(required=False, allow_null=True)
    # last_name = serializers.CharField(required=False, allow_null=True)
    # phone_no = serializers.CharField(required=False, allow_null=True)
    # birth_date = serializers.DateField(required=False, allow_null=True)
    roles = serializers.ReadOnlyField(source='get_user_roles', required=False)
    image = ProfileImageSerializer(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.Meta.excluded_fields:
            if not field_name in self.fields:
                continue
            self.fields.pop(field_name)

    class Meta (BaseUserSerializer.Meta):
        model = User
        fields = BaseUserSerializer.Meta.fields
        excluded_fields = ['password']
