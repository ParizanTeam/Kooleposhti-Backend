from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import Instructor, Student
from courses.filters import CourseFilter
from courses.pagination import DefaultPagination
from accounts.permissions import *
from ..models import *
from ..serializers import *
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from accounts.serializers.student_serializers import StudentSerializer
from skyroom import *
from Kooleposhti.settings import SKYROOM_KEY


api = SkyroomAPI(SKYROOM_KEY)


class SessionViewSet(ModelViewSet):
	serializer_class = SessionSerializer
	permission_classes = [IsInstructorOrReadOnly]
	http_method_names = ['get', 'post']

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
	search_fields = ['title', 'description', 
	'instructor__user__first_name', 'instructor__user__last_name']  # space comma seprator
	ordering_fields = ['price', 'last_update']  # -prince, last_update
	pagination_class = DefaultPagination  # can be moved to settings
	permission_classes = [IsInstructorOrReadOnly]

	def create(self, request, *args, **kwargs):
		data = request.data.copy()
		tags_data = data.pop('tags', [])
		goals_data = data.pop('goals', [])
		sessions_data = data.pop('sessions', [])
		if len(sessions_data):
			data['start_date'] = sessions_data[0]['date']
			data['end_date'] = sessions_data[-1]['date']
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		course = serializer.save()

		try:
			self.create_room(course)
		except Exception as e:
			course.delete()
			return Response({"SkyRoom": str(e)}, 
							status=status.HTTP_400_BAD_REQUEST)

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
		return Response(serializer.data, 
				status=status.HTTP_201_CREATED, headers=headers)


	def create_room(self, course):
		# create skyroom room and set the instructor operator
		params = {
			"name": f"class{course.id}",
			"title": course.title,
			"description": course.description,
			"session_duration": course.duration,
			"max_users": course.max_students + 1,
			"guest_login": False,
			"op_login_first": True
		}
		course.room_id = api.createRoom(params)
		params = {
			'room_id': course.room_id,
			'users': [
				{'user_id': course.instructor.user.userskyroom.skyroom_id, "access": 3}
			]
		}
		api.addRoomUsers(params)
		params = {
			'room_id': course.room_id,
			"language": "fa"
		}
		course.link = api.getRoomUrl(params)
		course.save()
		# params = {
		#     "room_id": course.room_id,
		#     "user_id": course.instructor.id,
		#     "nickname": course.instructor.user.username,
		#     "access": 3,
		#     "language": "fa",
		#     "ttl": 604800  #a week
		# }
		# url = api.getLoginUrl(params)
		# Link.objects.create(course=course, user=course.instructor.user, url=url)



	def update(self, request, *args, **kwargs):
		course_old = self.get_object()
		if course_old.is_owner(request.user.instructor):
			data = request.data.copy()
			tags_data = data.pop('tags', None)
			goals_data = data.pop('goals', None)
			sessions_data = data.pop('sessions', None)
			if sessions_data:
				data['start_date'] = sessions_data[0]['date']
				data['end_date'] = sessions_data[-1]['date']

			partial = kwargs.pop('partial', False)
			instance = self.get_object()
			serializer = self.get_serializer(instance, data=data, partial=partial)
			serializer.is_valid(raise_exception=True)
			course = serializer.save()

			try:
				self.update_room(course)
			except Exception as e:
				course = course_old
				course.save()
				return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

			if getattr(instance, '_prefetched_objects_cache', None):
				instance._prefetched_objects_cache = {}

			if tags_data:
				course.tags.all().delete()
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

		return Response("your'e not the course owner", status=status.HTTP_403_FORBIDDEN)



	def update_room(self, course):
		# update skyroom room
		params = {
			"room_id": course.room_id,
			"title": course.title,
			"description": course.description,
			"session_duration": course.duration,
			"max_users": course.max_students + 1
		}
		api.updateRoom(params)
		# if course.links_credit_date < course.end_date:
		#     for link in course.links:
		#         params = {
		#             "room_id": course.room_id,
		#             "user_id": link.user.id,
		#             "nickname": link.user.username,
		#             "access": 1,
		#             "language": "fa",
		#             "ttl": 604800  #a week
		#         }
		#         link.url = api.getLoginUrl(params)
		#         link.save()
		return course



	def delete_room(self, course):
		# delete skyroom room
		api.deleteRoom({"room_id": course.room_id})



	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.is_owner(request.user.instructor):

			try:
				self.delete_room(instance)
			except Exception as e:
				return Response({"SkyRoom": {"SkyRoom": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
				
			self.perform_destroy(instance)
			return Response(status=status.HTTP_204_NO_CONTENT)

		return Response("your'e not the course owner", status=status.HTTP_403_FORBIDDEN)



	def perform_add_student(self, course, student):
		# create room user
		params = {
			'room_id': course.room_id,
			'users': [{'user_id': student.user.userskyroom.skyroom_id}]
		}
		api.addRoomUsers(params)
		# params = {
		#     "room_id": course.room_id,
		#     "user_id": student.id,
		#     "nickname": student.user.username,
		#     "access": 1,
		#     "language": "fa",
		#     "ttl": 604800  #a week
		# }
		# url = api.getLoginUrl(params)
		# Link.objects.create(course=course, user=student.user, url=url)



	@action(detail=True, methods=['post'],
			permission_classes=[IsStudent])
	def enroll(self, request, *args, **kwargs):
		course = self.get_object()
		student = request.user.student
		if course.is_enrolled(student):
			return Response('Already enrolled', status=status.HTTP_400_BAD_REQUEST)
		if course.capacity < 1 or course.end_date < jdatetime.datetime.now():
			return Response("there's no enrollment available", status=status.HTTP_400_BAD_REQUEST)

		try:
			self.perform_add_student(course, student)
		except Exception as e:
			return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		course.students.add(student)
		course.update_capacity()
		return Response({'enrolled': True}, status=status.HTTP_200_OK)



	def perform_remove_student(self, course, student):
		# remove room user
		params = {
			'room_id': course.room_id,
			'users': [student.user.userskyroom.skyroom_id]
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

		try:
			self.perform_remove_student(course, student)
		except Exception as e:
			return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		course.students.remove(request.user.student)
		course.update_capacity()
		return Response({'left': True}, status=status.HTTP_200_OK)



	action(detail=True, methods=['put'],
			permission_classes=[IsInstructor], url_name="delete-student",
			url_path="delete-student/(?P<sid>[^/.]+)")
	def delete_student(self, request: HttpRequest, sid, *args, **kwargs):
		course = self.get_object()
		instructor = request.user.instructor
		if course.is_owner(instructor):
			student = get_object_or_404(Student, pk=sid)
			if not course.is_enrolled(student):
				return Response('Not enrolled', status=status.HTTP_403_FORBIDDEN)

			try:
				self.perform_remove_student(course, student)
			except Exception as e:
				return Response({"SkyRoom": str(e)}, status=status.HTTP_400_BAD_REQUEST)

			course.students.remove(student)
			course.update_capacity()
			return Response({'deleted': True})
		return Response("your'e not the course owner", status=status.HTTP_403_FORBIDDEN)



	@action(detail=True, permission_classes=[IsAuthenticated],
			url_name="get-students", url_path="students")
	def get_students(self, request, *args, **kwargs):
		course = self.get_object()
		user = request.user
		if course.is_course_user(user):
			serializer = StudentSerializer(course.students, many=True)
			return Response(status=status.HTTP_200_OK, data=serializer.data)
		return Response("your don't have permission to perform this action", status=status.HTTP_403_FORBIDDEN)



	@action(detail=True, permission_classes=[AllowAny],
			url_name="can-enroll", url_path="can-enroll")
	def can_enroll(self, request, *args, **kwargs):
		course = self.get_object()
		try:
			return Response({'enroll': not course.is_enrolled(request.user.student) 
				and course.end_date >= jdatetime.date.today()}, status=status.HTTP_200_OK)
		except:
			return Response({'enroll': not request.user.is_authenticated
				and course.end_date >= jdatetime.date.today()}, status=status.HTTP_200_OK)

		
	@action(detail=True, permission_classes=[AllowAny],
			url_name="role", url_path="role")
	def get_role(self, request, *args, **kwargs):
		user = request.user
		course = self.get_object()
		role = 'anonymous'
		if user.is_authenticated and user.has_role('student') and course.is_enrolled(user.student):
			role = 'student'
		if user.is_authenticated and user.has_role('instructor') and course.is_owner(user.instructor):
			role = 'teacher'
		return Response({"role": role}, status=status.HTTP_200_OK)


	@action(detail=True, permission_classes=[IsAuthenticated])
	def link(self, request, *args, **kwargs):
		course = self.get_object()
		user = request.user
		if course.is_course_user(user):
			link = course.links.get(user=user).url
			return Response(link, status=status.HTTP_200_OK)

		return Response("you're not enrolled", status=status.HTTP_403_FORBIDDEN)


	@action(detail=True, methods=['post'],
			permission_classes=[IsStudent])
	def rate(self, request, *args, **kwargs):
		course = self.get_object()
		student = request.user.student
		if course.is_enrolled(student):
			rate_data = request.data['rate']
			try:
				rate_obj = Rate.objects.get(course=course, student=student)
				rate_obj.rate = rate_data
				rate_obj.save()
				course.update_rate()
				return Response('you changed your rate.', status=status.HTTP_200_OK)
			except:
				Rate.objects.create(
					course=course, student=student, rate=rate_data)
				# course.rate = round((course.rate * course.rate_no + rate_data) / (course.rate_no + 1), 1)
				# course.rate_no += 1
				# course.save()
				course.update_rate()
				return Response('rated successfully', status=status.HTTP_200_OK)
		else:
			return Response({"you're not enrolled."}, status=status.HTTP_403_FORBIDDEN)

	
	@action(detail=True, permission_classes=[IsAuthenticated])
	def assignments(self, request, *args, **kwargs):
		course = self.get_object()
		user = request.user
		if course.is_course_user(user):
			serializer = AssignmentSerializer(course.assignments, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response({"you do not have permission to see this course assignments."}, 
						status=status.HTTP_403_FORBIDDEN)




	@action(detail=True, methods=['GET'],
			permission_classes=[IsStudent],url_path="favorite/add")
	def add_favorite(self, request, *args, **kwargs):
		course = self.get_object()
		student = request.user.student
		Favorite.objects.create(course=course, student=student)
		return Response('Added to favorites successfully', status=status.HTTP_200_OK)


	@action(detail=True, methods=['GET'],
			permission_classes=[IsStudent],url_path="favorite/remove")
	def remove_favorite(self, request, *args, **kwargs):
		course = self.get_object()
		student = request.user.student
		favorite=Favorite.objects.get(course=course, student=student)
		if(not favorite.exists()):
			return Response('Course in not in favorites', status=status.HTTP_400_BAD_REQUEST)
		favorite.delete()
		return Response('Removed from favorites successfully', status=status.HTTP_200_OK)


	
	@action(detail=False, permission_classes=[AllowAny])
	def top(self, request):
		count = request.data.get('count', 10)
		count = min(len(Course.objects.all()), count)
		serializer = SimpleCourseSerializer(Course.objects.order_by('pk')[:count], many=True)
		return Response(status=status.HTTP_200_OK, data=serializer.data)



	# @action(detail=True, methods=['post'],
	# 		permission_classes=[IsAuthenticated])
	# def comment(self, request, *args, **kwargs):
	# 	course = self.get_object()
	# 	user = request.user
	# 	if course.is_course_user(user):
	# 		Comment.objects.create(course=course, student=user.student,
	# 							   text=request.data['comment'])
	# 		return Response('succssesfuly commented', status=status.HTTP_200_OK)
	# 	return Response("you're not enrolled", status=status.HTTP_403_FORBIDDEN)



class CategoryViewSet(ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [IsAdminOrReadOnly]

	@action(detail=True, url_path="courses")
	def get_courses(self, request, *args, **kwargs):
		category = self.get_object()
		serializer = self.get_serializer(category.courses, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


