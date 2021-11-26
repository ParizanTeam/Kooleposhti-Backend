from accounts.models import User
from rest_framework import serializers
from images.serializers import ProfileImageSerializer
from courses.serializers import CourseSerializer


class BasePublicProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='publicprofile.bio', required=False)
    image = ProfileImageSerializer(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'image']
        read_only_fields = ['first_name', 'last_name', 'username', 'image']


class StudentPublicProfileSerializer(BasePublicProfileSerializer):
    age = serializers.IntegerField(
        source='student.age', min_value=0, max_value=18, required=False)

    class Meta (BasePublicProfileSerializer.Meta):
        fields = BasePublicProfileSerializer.Meta.fields + ['age']


class InstructorPublicProfileSerializer(BasePublicProfileSerializer):
    rate = serializers.IntegerField(
        source='instructor.rate', min_value=0, max_value=5, required=False, read_only=True)
    courses = CourseSerializer(
        source='instructor.courses', many=True, required=False, read_only=True)

    class Meta (BasePublicProfileSerializer.Meta):
        fields = BasePublicProfileSerializer.Meta.fields + ['rate', 'courses']
        read_only_fields = BasePublicProfileSerializer.Meta.read_only_fields + \
            ['rate', 'courses']
