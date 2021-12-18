from rest_framework.response import Response
from accounts.permissions import *
from ..models import Assignment, Homework, Feedback, Course
from ..serializers import AssignmentSerializer, HomeworkSerializer,\
FeedbackSerializer, HomeworkImageSerializer
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny



class AssignmentViewSet(ModelViewSet):
	queryset = Assignment.objects.select_related('course').all()
	serializer_class = AssignmentSerializer
	permission_classes = [IsInstructorOrStudentReadOnly]


	def list(self, request, *args, **kwargs):
		return self.perform_get(request, 'list', *args, **kwargs)

	def retrieve(self, request, *args, **kwargs):
		return self.perform_get(request, 'retrieve', *args, **kwargs)

	def create(self, request, *args, **kwargs):
		instructor = request.user.instructor
		course_pk = request.data['course']
		course = Course.objects.get(pk=course_pk)
		if not course.is_owner(instructor):
			return Response('you are not the course owner.', 
							status=status.HTTP_403_FORBIDDEN)
		return super().create(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		return self.perform_change(request, 'update', *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		return self.perform_change(request, 'destroy', *args, **kwargs)

	
	def perform_get(self, request, action, *args, **kwargs):
		assignment = self.get_object()
		user = request.user
		if not (user.has_role('student') and assignment.is_course_student(user.student)) \
		and not (user.has_role('instructor') and  assignment.is_course_owner(user.instructor)):
			return Response('you are not enrolled.',status=status.HTTP_403_FORBIDDEN)
		if action == 'retrieve':
			return super().retrieve(request, *args, **kwargs)
		return super().list(request, *args, **kwargs)


	def perform_change(self, request, action, *args, **kwargs):
		instructor = request.user.instructor
		assignment = self.get_object()
		if not assignment.is_course_owner(instructor):
			return Response('you are not the course owner.', 
							status=status.HTTP_403_FORBIDDEN)
		if action == 'update':
			return super().update(request, *args, **kwargs)
		return super().destroy(request, *args, **kwargs)


	# @action(detail=True, url_path='mysubmit',
	# 		 permission_classes=[IsStudent])
	# def get_homework(self, request, *args, **kwargs):
	# 	student = request.user.student
	# 	assignment = self.get_object()
	# 	course = assignment.course
	# 	if not course.is_enrolled(student):
	# 		return Response('you are not enrolled.', 
	# 						status=status.HTTP_403_FORBIDDEN)		
	# 	homework = assignment.homeworks.filter(student=student)
	# 	serializer = HomeworkSerializer(instance=homework)
	# 	return Response(serializer.data, status=status.HTTP_200_OK)


class HomeworkViewSet(ModelViewSet):
	queryset = Homework.objects.select_related('assignment').all()
	serializer_class = HomeworkSerializer
	permission_classes = [IsStudentOrInstructorReadOnly]

	def get_queryset(self):
		return Homework.objects.filter(
						assignment_id=self.kwargs.get('assignment_pk'))

	def get_serializer_context(self):
		return {'assignment': self.kwargs.get('assignment_pk')}

	def list(self, request, *args, **kwargs):
		homework = self.get_object()
		user = request.user
		if user.has_role('instructor') and homework.is_course_owner(user.instructor):
			return super().list(request, *args, **kwargs)
		return Response('you are not the course owner.',
						status=status.HTTP_403_FORBIDDEN)

	def retrieve(self, request, *args, **kwargs):
		homework = self.get_object()
		user = request.user
		if (user.has_role('student') and homework.is_owner(user.student)) \
		or (user.has_role('instructor') and homework.is_course_owner(user.instructor)):
			return super().retrieve(request, *args, **kwargs)
		return Response('you do not have permission to see this homework.',
						status=status.HTTP_403_FORBIDDEN)


	def create(self, request, *args, **kwargs):
		data = request.data.copy()
		student = request.user.student
		assignment_pk = self.kwargs.get('assignment_pk')
		try:
			assignment = Assignment.objects.get(pk=assignment_pk)
		except:
			return Response('assignment Not found', status=status.HTTP_404_NOT_FOUND)
		if not assignment.is_course_student(student):
			return Response('Not enrolled yet!', status=status.HTTP_403_FORBIDDEN)
		if not data['answer'] and not data['file']:
			return Response('please submit an answer.', status=status.HTTP_400_BAD_REQUEST)
		if assignment.homeworks.filter(student=student).exists():
			return Response('you already submited an answer.', 
							status=status.HTTP_400_BAD_REQUEST)
		data['student'] = student.pk
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


	def update(self, request, *args, **kwargs):
		return self.perform_change(request, 'update', *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		return self.perform_change(request, 'destroy', *args, **kwargs)


	def perform_change(self, request, action, *args, **kwargs):
		student = request.user.student
		homework = self.get_object()
		if not homework.is_owner(student):
			return Response('you do not have permission to change this homework.',
							 status=status.HTTP_403_FORBIDDEN)
		if action == 'update':
			return super().update(request, *args, **kwargs)
		return super().destroy(request, *args, **kwargs)


	# @action(detail=True, methods=['post'],
	# 		permission_classes=[IsInstructor])
	# def grade(self, request, *args, **kwargs):
	# 	instructor = request.user.instructor
	# 	homework = self.get_object()
	# 	if not homework.is_course_owner(instructor):
	# 		return Response('you are not the course owner.', 
	# 						status=status.HTTP_403_FORBIDDEN)		
	# 	homework.grade = request.data['grade']
	# 	homework.save()
	# 	return Response('successfuly graded.', status=status.HTTP_200_OK)	


	@action(detail=False, permission_classes=[IsStudent])
	def me(self, request, *args, **kwargs):
		student = request.user.student
		assignment_pk = self.kwargs.get('assignment_pk')
		try:
			assignment = Assignment.objects.get(pk=assignment_pk)
		except:
			return Response('assignment Not found.', 
							status=status.HTTP_404_NOT_FOUND)
		if not assignment.course.is_enrolled(student):
			return Response('you are not enrolled.', 
							status=status.HTTP_403_FORBIDDEN)		
		homework = assignment.homeworks.filter(student=student).first()
		if homework:
			serializer = self.get_serializer(instance=homework)
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(status=status.HTTP_200_OK)



class FeedbackViewSet(ModelViewSet):
	queryset = Assignment.objects.select_related('homework').all()
	serializer_class = FeedbackSerializer
	permission_classes = [IsInstructorOrStudentReadOnly]

	# @action(detail=False, url_path="/",
	# methods=['get', 'post', 'patch', 'delete'],
	# permission_classes=[IsInstructorOrStudentReadOnly])
	# def feedback(self, request, *args, **kwargs):
	# 	if request.method == 'get':
	# 		return self.retrieve(request)
	# 	if request.method == 'post':
	# 		return self.create(request)
	# 	if request.method == 'patch':
	# 		return self.perform_action(request, 'update')
	# 	if request.method == 'delete':
	# 		return self.perform_action(request, 'destroy')
			

	def get_queryset(self):
		return Feedback.objects \
		.filter(homework_id=self.kwargs.get('homework_pk'))

	def get_serializer_context(self):
		return {'homework': self.kwargs.get('homework_pk')}

	def list(self, request, *args, **kwargs):
		feedback = self.get_object()
		user = request.user
		if user.has_role('instructor') and feedback.is_course_owner(user.instructor):
			return super().list(request, *args, **kwargs)
		return Response('you are not the course owner.',
						status=status.HTTP_403_FORBIDDEN)

	def retrieve(self, request, *args, **kwargs):
		feedback = self.get_object()
		user = request.user
		if (user.has_role('student') and feedback.is_mine(user.student)) \
		or (user.has_role('instructor') and feedback.is_owner(user.instructor)):
			return super().retrieve(request, *args, **kwargs)
		return Response('you are not enrolled.',status=status.HTTP_403_FORBIDDEN)		


	def create(self, request, *args, **kwargs):
		instructor = request.user.instructor
		homework_pk = self.kwargs.get('homework_pk')
		try:
			homework = Homework.objects.get(pk=homework_pk)
		except:
			return Response('homework Not found', status=status.HTTP_404_NOT_FOUND)
		print(homework.answer)
		if not homework.is_course_owner(instructor):
			return Response('you are not the course owner.', 
							status=status.HTTP_403_FORBIDDEN)
		return super().create(request, *args, **kwargs)


	def update(self, request, *args, **kwargs):
		return self.perform_change(request, 'update', *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		return self.perform_change(request, 'destroy', *args, **kwargs)

	def perform_change(self, request, action, *args, **kwargs):
		instructor = request.user.instructor
		feedback = self.get_queryset()[0]
		if not feedback.is_course_owner(instructor):
			return Response('you are not the course owner.', 
							status=status.HTTP_403_FORBIDDEN)
		if action == 'update':
			return super().update(request, *args, **kwargs)
		return super().destroy(request, *args, **kwargs)