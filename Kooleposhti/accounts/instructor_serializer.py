from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import html, model_meta, representation
from .models import Instructor, Tag
from rest_framework import serializers
from .user_serializers import BaseUserSerializer


class TagProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class InstructorProfileSerializer(BaseUserSerializer):
    tags = TagProfileSerializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = Instructor
        fields = ['id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'phone_no', 'roles', ] + \
            ['tags', 'user_id', ]
        excluded_fields = ['birth_date']
