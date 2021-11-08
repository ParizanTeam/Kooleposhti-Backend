from rest_framework import serializers
from courses.models import Course
from .models import Student
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import html, model_meta, representation
from .models import Instructor, Tag
from rest_framework import serializers
from .serializers import update_relation
from .user_serializers import BaseUserSerializer


class StudentSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Student
        fields = BaseUserSerializer.Meta.fields + ['user_id', ]


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', ]
