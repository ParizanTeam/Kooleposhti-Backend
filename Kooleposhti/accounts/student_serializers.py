from rest_framework import serializers

from courses.models import Course
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user.username')
    email = serializers.EmailField(read_only=True, source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_no = serializers.CharField(source='user.phone_no')
    birth_date = serializers.DateField(source='user.birth_date')

    class Meta:
        model = Student
        fields = ['id', 'user_id', 'username', 'email',
                  'first_name', 'last_name', 'phone_no', 'birth_date']


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', ]
