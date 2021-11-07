from .models import Instructor, Tag
from rest_framework import serializers


class TagProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class InstructorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user.username')
    email = serializers.EmailField(read_only=True, source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_no = serializers.CharField(source='user.phone_no')
    birth_date = serializers.DateField(source='user.birth_date')
    tags = TagProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Instructor
        fields = ('id', 'user_id', 'username', 'email',
                  'first_name', 'last_name', 'phone_no', 'birth_date', 'tags')
