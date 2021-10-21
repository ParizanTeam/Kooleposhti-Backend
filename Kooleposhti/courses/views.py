from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Instructor, Student
from courses.filters import CourseFilter
from courses.pagination import DefaultPagination
from .models import Course, Review
from .serializers import CourseSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class CourseList(ModelViewSet):
    queryset = Course.objects.select_related('instructor').all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['instructor_id']
    filterset_class = CourseFilter
    search_fields = ['title', 'description']  # space comma seprator
    ordering_fields = ['price', 'last_update']  # -prince, last_update
    pagination_class = DefaultPagination  # can be moved to settings


class ReviewViweSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(course_id=self.kwargs['course_pk'])

    def get_serializer_context(self):
        return {
            'course_id': self.kwargs['course_pk']
        }


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
