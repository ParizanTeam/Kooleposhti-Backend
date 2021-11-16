from courses.serializers import CourseSerializer
from rest_framework import serializers
from accounts.instructor_serializer import InstructorProfileSerializer
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
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    courses = CourseSerializer(many=True, read_only=True)

    class Meta (BaseUserSerializer.Meta):
        model = Instructor
        fields = ['first_name', 'courses']
        # write_only_fields = ['id', ]


class StudentEnrollLeaveCourseSerializer(serializers.ModelSerializer):
    course_pk = serializers.IntegerField(write_only=True, source='id')

    class Meta:
        model = Course
        fields = ['course_pk', ]
