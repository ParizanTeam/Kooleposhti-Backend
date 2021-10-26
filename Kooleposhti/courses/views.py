from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import Instructor, Student
from courses.filters import CourseFilter
from courses.pagination import DefaultPagination
from accounts.permissions import IsAdminOrReadOnly
from .models import CartItem, Course, Review, ShoppingCart
from .serializers import CartItemSerializer, CourseSerializer, ReviewSerializer, ShoppingCartSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.select_related('instructor').all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['instructor_id']
    filterset_class = CourseFilter
    search_fields = ['title', 'description']  # space comma seprator
    ordering_fields = ['price', 'last_update']  # -prince, last_update
    pagination_class = DefaultPagination  # can be moved to settings
    permission_classes = [IsAdminOrReadOnly]


class ReviewViweSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(course_id=self.kwargs.get('course_pk'))

    def get_serializer_context(self):
        return {
            'course_id': self.kwargs.get('course_pk')
        }


class ShoppingCartViewSet(CreateModelMixin, RetrieveModelMixin,
                          DestroyModelMixin, GenericViewSet):
    queryset = ShoppingCart.objects.prefetch_related('items__course').all()
    serializer_class = ShoppingCartSerializer


class ShoppingCartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects \
            .filter(pk=self.kwargs.get('pk')) \
            .select_related('course')

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
                    price=12.23, instructor=Instructor.objects.first())
    course.save()
    item1 = CartItem(cart=ShoppingCart.objects.first(),
                     course=Course.objects.first(),
                     quantity=3)
    item1.save()
    '''
    {
        "id": 1,
        "username": "user2",
        "email": "user2@gmail.com",
        "first_name": "user2",
        "last_name": "test"
        'password' : adminrootadmin
    }
    '''


# def instructor_detail(request, pk):
#     return Response('ok')
