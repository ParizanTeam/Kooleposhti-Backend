from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Instructor, Student
from .models import Course
from .serializers import CourseSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet


class CourseList(ListCreateAPIView):
    queryset = Course.objects.select_related('instructor').all()
    serializer_class = CourseSerializer


class CourseDetail(APIView):
    pass


# @api_view(['GET', 'POST'])
# def course_list(request):
#     if request.method == 'GET':
#         queryset = Course.objects.all()
#         serializer = CourseSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CourseSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.validated_data)


# @api_view()
# def course_detail(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     serializer = CourseSerializer(course)
#     return Response(serializer.data)
'''    
    try:
        course = Course.objects.get(pk=id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
'''


def add_test_data():
    instructor = Instructor(first_name='test instructor', last_name='test last_name for instructor',
                            email='test_instructor@gmail.com', phone='9999213', birth_date=None)
    instructor.save()
    student = Student(first_name='test student', last_name='test last_name for student',
                      email='test_student@gmail.com', phone='1111213', birth_date=None)
    student.save()
    course = Course(title='Testt Course', description='Description for Course',
                    price=12.23, instructor=instructor)
    course.save()


# def instructor_detail(request, pk):
#     return Response('ok')
