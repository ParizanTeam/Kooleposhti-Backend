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
from accounts.student_serializers import StudentSerializer
from skyroom import *
from Kooleposhti.settings import skyroom_key


api = SkyroomAPI(skyroom_key)


class SessionViewSet(ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [IsInstructorOrReadOnly]
    # permission_classes = [AllowAny]

    def get_queryset(self):
        return Session.objects.filter(course_id=self.kwargs.get('course_pk'))
        
    def get_serializer_context(self):
        return {'course': self.kwargs.get('course_pk')}



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

    def create(self, request, *args, **kwargs):
        data = request.data
        tags_data = data.pop('tags', [])
        goals_data = data.pop('goals', [])
        sessions_data = data.get('sessions')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        try:
            course = self.perform_create(serializer)
        except Exception as e: 
            return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        for tag in tags_data:
            # Tag.objects.create(course=course, **tag)
            tag['course'] = course.pk
            new_tag = TagSerializer(data=tag)
            new_tag.is_valid(raise_exception=True)
            new_tag.save()
        for goal in goals_data:
            goal['course'] = course.pk
            new_goal = GoalSerializer(data=goal)
            new_goal.is_valid(raise_exception=True)
            new_goal.save()
        for session in sessions_data:
            new_session = SessionSerializer(data=session)
            new_session.context['course'] = course.pk
            new_session.is_valid(raise_exception=True)
            new_session.save()
        course = Course()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



    def perform_create(self, serializer):
        # create skyroom room and set the instructor operator
        course = serializer.save()
        # params = {
        #     "name": f"c{course.id}",
        #     "title": course.title,
        #     "description": course.description,
        #     "session_duration": course.duration,
        #     "max_users": course.max_students + 1,
        #     "guest_login": False,
        #     "op_login_first": True
        # }
        # try:
        #     course.room_id = api.createRoom(params)
        #     instructor = api.getUser({"username":course.instructor.user.username})
        #     params = {           
        #         'room_id': course.room_id,
        #         'users': [ 
        #             {'user_id': instructor['id'], "access": 3}
        #         ]
        #     }
        #     api.addRoomUsers(params)
        # except Exception as e:
        #     course.delete()
        #     raise e

        return course



    def update(self, request, *args, **kwargs):
        data = request.data
        tags_data = data.pop('tags', None)
        goals_data = data.pop('goals', None)
        sessions_data = data.get('sessions', None)
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # if not just image
        if len(data) > 1 or not 'image' in data:
            try:
                course = self.perform_update(serializer)
            except Exception as e: 
                return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        if tags_data:
            self.tags.all().delete()   
            for tag in tags_data:
                tag['course'] = course.pk
                new_tag = TagSerializer(data=tag)
                new_tag.is_valid(raise_exception=True)
                new_tag.save()
        if goals_data:
            course.goals.all().delete()
            for goal in goals_data:
                goal['course'] = course.pk
                new_goal = GoalSerializer(data=goal)
                new_goal.is_valid(raise_exception=True)
                new_goal.save()
        if sessions_data:
            course.sessions.all().delete()
            for session in sessions_data:
                new_session = SessionSerializer(data=session)
                new_session.context['course'] = course.pk
                new_session.is_valid(raise_exception=True)
                new_session.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)



    def perform_update(self, serializer):
        course_old = self.get_object()
        course = serializer.save()
        # update skyroom room
        # try:
        #     # room = api.getRoom({"name": f"c{course.id}"})
        #     params = {
        #         "room_id": course.room_id,
        #         "title": course.title,
        #         "description": course.description,
        #         "session_duration": course.duration,
        #         "max_users": course.max_students + 1
        #     }
        #     api.updateRoom(params)
        # except Exception as e:
        #     course = course_old
        #     course.save()
        #     raise e
            
        return course




    def perform_destroy(self, instance):
        # delete skyroom room 
        # room = api.getRoom({"name": f"c{instance.pk}"})
        # api.deleteRoom({"room_id": instance.room_id})
        return super().perform_destroy(instance)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
        except Exception as e: 
            return Response({"SkyRoom": {"SkyRoom": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)



    def perform_add_student(self, course, student):
        # create room user
        # room = api.getRoom({"name": f'c{course.pk}'})
        room_student = api.getUser({"username": student.user.username})
        params = {           
            'room_id': course.room_id,
            'users': [{'user_id': room_student['id']}]
        }
        api.addRoomUsers(params)



    @action(detail=True, methods=['post'],
            permission_classes=[IsStudent])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        student = request.user.student
        if course.is_enrolled(student):
            return Response('Already enrolled', status=status.HTTP_400_BAD_REQUEST)
        if course.capacity < 1:
            return Response("there's no enrollment available", status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     self.perform_add_student(course, student)
        # except Exception as e: 
        #     return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        course.students.add(student)
        course.update_capacity()
        return Response({'enrolled': True}, status=status.HTTP_200_OK)



    def perform_remove_student(self, course, student):
        # remove room user
        # room = api.getRoom({"name": f'c{course.pk}'})
        room_student = api.getUser({"username": student.user.username})
        params = {           
            'room_id': course.room_id,
            'users': [room_student['id']]
        }
        api.removeRoomUsers(params)


    
    @action(detail=True, methods=['post'],
            permission_classes=[IsStudent], url_name="leave", 
            url_path="leave")
    def leave(self, request: HttpRequest, *args, **kwargs):
        course = self.get_object()
        student = request.user.student
        if not course.is_enrolled(student):
            return Response('Not enrolled yet.', status=status.HTTP_400_BAD_REQUEST)
        
        # try:
        #     self.perform_remove_student(course, student)
        # except Exception as e: 
        #     return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        course.students.remove(request.user.student)
        course.update_capacity()
        return Response({'left': True}, status=status.HTTP_200_OK)



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

            # try:
            #     self.perform_remove_student(course, student)
            # except Exception as e: 
            #     return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            course.students.remove(student)
            course.update_capacity()
            return Response({'deleted': True})
        else:
            return Response("your'e not the course owner", status=status.HTTP_403_FORBIDDEN)



    @action(detail=True, permission_classes=[IsInstructor], 
            url_name="get-students", url_path="students")
    def get_students(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = StudentSerializer(course.students, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, permission_classes=[AllowAny], 
            url_name="can-enroll", url_path="can-enroll")
    def can_enroll(self, request, *args, **kwargs):
        course = self.get_object()
        try:
            return Response({'enroll': not course.is_enrolled(request.user.student)}, 
                            status=status.HTTP_200_OK)
        except:
            return Response({'enroll': not request.user.is_authenticated}, 
                            status=status.HTTP_200_OK)


    
    @action(detail=True, permission_classes=[IsAuthenticated])
    def link(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        if (user.has_role('student') and course.is_enrolled(user.student)) \
        or (user.has_role('instructor') and course.is_owner(user.instructor)):            
            try:
                # room = api.getRoom({"name": f'c{course.pk}'})
                params = {           
                    'room_id': course.room_id,
                    "language": "fa"
                }
                response = api.getRoomUrl(params)
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e: 
                return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response("you're not enrolled", status=status.HTTP_403_FORBIDDEN)


    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def comment(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        if (user.has_role('student') and course.is_enrolled(user.student)):
        # or (user.has_role('instructor') and course.is_owner(user.instructor)):
            Comment.objects.create(course=course, student=user.student, 
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
                return Response('you changed rour rate.', status=status.HTTP_200_OK)
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
    permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [AllowAny]

    @action(detail=True, url_path="courses")
    def get_courses(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category.courses, many=True)
        return Response(serializer.data)


# class TagViewSet(ModelViewSet):
#     serializer_class = TagSerializer
#     permission_classes = [IsInstructorOrReadOnly]

#     def get_queryset(self):
#         return Tag.objects.filter(course_id=self.kwargs.get('course_pk'))
        
#     def get_serializer_context(self):
#         return {'course': self.kwargs.get('course_pk')}
        


# class GoalViewSet(ModelViewSet):
#     serializer_class = TagSerializer
#     # permission_classes = [IsAdminOrReadOnly]
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         return Goal.objects.filter(course_id=self.kwargs.get('course_pk'))
        
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
