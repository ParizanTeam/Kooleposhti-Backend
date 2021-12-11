from .models import MyImage
from rest_framework import serializers


class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyImage
        fields = ['image', 'name', 'description', 'upload_date']


class HomeworkImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyImage
        fields = ['image']
