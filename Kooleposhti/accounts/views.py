from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from accounts.models import Instructor, Student
from .serializers import InstructorSerializer, StudentSerializer
from rest_framework.generics import ListAPIView
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response



class StudentViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class InstructorList(ListAPIView):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer

    def get_serializer_context(self):
        return {
            'request': self.request
        }
