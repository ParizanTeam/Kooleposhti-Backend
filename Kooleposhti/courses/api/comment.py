from rest_framework.response import Response
from accounts.permissions import *
from ..models import *
from ..serializers import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly




class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related('course').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(
            course_id=self.kwargs.get('course_pk'), parent=None)

	def get_serializer_context(self):
		return {'course': self.kwargs.get('course_pk')}


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
		return self.perform_action(request, 'update')


	def destroy(self, request, *args, **kwargs):
		return self.perform_action(request, 'destroy')


	def perform_action(self, request, action, *args, **kwargs):
		student = request.user.student
		homework = self.get_object()
		if not homework.is_owner(student):
			return Response('you do not have permission to change this homework.',
							 status=status.HTTP_403_FORBIDDEN)
		if action == 'update':
			return super().update(request, *args, **kwargs)
		return super().destroy(request, *args, **kwargs)
