from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from images.serializers import ProfileImageSerializer
from .models import MyImage


class ImageViewSet(ModelViewSet):
    queryset = MyImage.objects.all()
    serializer_class = ProfileImageSerializer
