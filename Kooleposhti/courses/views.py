from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import Instructor, Student
from courses.filters import CourseFilter
from courses.pagination import DefaultPagination
from accounts.permissions import *
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class SessionViewSet(ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [IsInstructorOrReadOnly]
    # permission_classes = [AllowAny]

    def get_queryset(self):
        return Tag.objects.filter(course_id=self.kwargs.get('course_pk'))
        
    # def get_serializer_context(self):
    #     return {'course_id': self.kwargs.get('course_pk')}

    # @action(detail=True, methods=['post'],
    #         permission_classes=[AllowAny])
    # def enroll(self, request, *args, **kwargs):
    #     myclass = self.get_object()
    #     myclass.students.add(request.user)
    #     myclass.course.students.add(request.user)
    #     return Response({'enrolled': True})


    # @action(detail=True, methods=['delete'],
    #         permission_classes=[AllowAny])
    # def leave(self, request: HttpRequest, *args, **kwargs):
    #     myclass = self.get_object()
    #     myclass.students.delete(request.user)
    #     myclass.course.students.delete(request.user)
    #     return Response({'left': True})




class CourseViewSet(ModelViewSet):
    # queryset = Course.objects.select_related('instructor').all()
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['instructor_id']
    filterset_class = CourseFilter
    search_fields = ['title', 'description']  # space comma seprator
    ordering_fields = ['price', 'last_update']  # -prince, last_update
    pagination_class = DefaultPagination  # can be moved to settings
    permission_classes = [IsInstructorOrReadOnly]
    # permission_classes = [AllowAny]


    @action(detail=True, methods=['put'],
            permission_classes=[IsStudent])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        if course.is_enrolled(request.user):
            return Response('Already enrolled', status=status.HTTP_400_BAD_REQUEST)
        course.students.add(request.user)
        return Response({'enrolled': True}, status=status.HTTP_200_OK)

    
    @action(detail=True, methods=['put'],
            permission_classes=[IsStudent], url_name="leave", 
            url_path="leave")
    def leave(self, request: HttpRequest, *args, **kwargs):
        course = self.get_object()
        if not course.is_enrolled(request.user):
            return Response('Not enrolled', status=status.HTTP_400_BAD_REQUEST)
        course.students.remove(request.user)
        return Response({'left': True}, status=status.HTTP_200_OK)


    @action(detail=True, permission_classes=[IsInstructor], 
            url_name="get-students", url_path="students")
    def get_students(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course.students, many=True)
        return Response(serializer.data)


    @action(detail=True, permission_classes=[AllowAny], 
            url_name="get-students", url_path="classes")
    def get_classes(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course.classes, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['put'],
            permission_classes=[IsInstructor], url_name="delete-student", 
            url_path="delete-student/(?P<sid>[^/.]+)")
    def delete_student(self, request: HttpRequest, sid, *args, **kwargs):
        course = self.get_object()
        instructor = request.user.instructor
        if course.is_owner(instructor):
            student = get_object_or_404(Student, pk=sid)
            if not course.is_enrolled(student):
                return Response('Not enrolled', status=status.HTTP_400_BAD_REQUEST)
            course.students.remove(student)
            return Response({'deleted': True})
        else:
            return Response("your'e not the course owner", status=status.HTTP_403_FORBIDDEN)


    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def comment(self, request, *args, **kwargs):
        course = self.get_object()
        if course.is_enrolled(request.user.student) or course.is_owner(request.user.instructor):
            Comment.objects.create(course=course, student=request.user, 
                                        text=request.data['comment'])
            return Response('succssesfuly commented', status=status.HTTP_200_OK)
        return Response("you're not enrolled", status=status.HTTP_403_FORBIDDEN)


    @action(detail=True, methods=['post'],
            permission_classes=[IsStudent])
    def rate(self, request, *args, **kwargs):
        course = self.get_object()
        student = request.user.student
        if course.is_enrolled(student):
            rate_data = request.data['rate']
            try:
                rate_obj = Rate.objects.filter(course=course, student=student)
                rate_obj.rate = rate_data
                rate_obj.save()
                return Response('you change rour rate.', status=status.HTTP_200_OK)
            except:
                Rate.objects.create(course=course, student=student, rate=rate_data)
                # course.rate = round((course.rate * course.rate_no + rate_data) / (course.rate_no + 1), 1)
                # course.rate_no += 1
                # course.save()
                return Response('rated successfully', status=status.HTTP_200_OK)
            course.update_rate()
        else:
            return Response({"you're not enrolled."}, status=status.HTTP_403_FORBIDDEN)



# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     # permission_classes = [IsAdminOrReadOnly]
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         return Comment.objects.filter(course_id=self.kwargs.get('course_pk'))

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [AllowAny]

    @action(detail=True)
    def get_courses(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category.courses, many=True)
        return Response(serializer.data)


# class TagViewSet(ModelViewSet):
    # serializer_class = TagSerializer
    # permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return Tag.objects.filter(course_id=self.kwargs.get('course_pk'))
        


# class GoalViewSet(ModelViewSet):
#     serializer_class = TagSerializer
#     # permission_classes = [IsAdminOrReadOnly]
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         return Goal.objects.filter(course_id=self.kwargs.get('course_pk'))
        
#     def get_serializer_context(self):
#         return {'course_id': self.kwargs.get('course_pk')}



# class ChapterViewSet(ModelViewSet):
#     serializer_class = ChapterSerializer
#     permission_classes = [IsAdminOrReadOnly]
#     def get_queryset(self):
#         return Chapter.objects.filter(course_id=self.kwargs.get('course_pk'))

#     def get_serializer_context(self):
#         return {'course_id': self.kwargs.get('course_pk')}


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
