from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import html, model_meta, representation
from accounts.models import Instructor, Tag
from rest_framework import serializers
from .user_serializers import BaseUserSerializer


class TagProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class InstructorProfileSerializer(BaseUserSerializer):
    tags = TagProfileSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.Meta.excluded_fields:
            if not field_name in self.fields:
                continue
            self.fields.pop(field_name)

    class Meta(BaseUserSerializer.Meta):
        model = Instructor
        fields = BaseUserSerializer.Meta.fields + ['tags', 'user_id', ]
        excluded_fields = ['birth_date']


class InstructorSerializer(BaseUserSerializer):
    tags = TagProfileSerializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = Instructor
        fields = ['id', 'username', 'first_name', 'last_name',
                  'image', 'tags']
