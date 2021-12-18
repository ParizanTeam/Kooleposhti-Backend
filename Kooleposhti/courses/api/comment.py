from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from accounts.permissions import *
from ..models import *
from ..serializers import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q




class CommentViewSet(ModelViewSet):
	queryset = Comment.objects.select_related('course').all()
	serializer_class = CommentSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		return Comment.objects.filter(
			course_id=self.kwargs.get('course_pk'), parent=None)
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['course'] = self.kwargs.get('course_pk')
		return context


	def create(self, request, *args, **kwargs):
		user = request.user
		course = get_object_or_404(Course.objects, pk=self.kwargs.get('course_pk'))
		if not course.is_course_user(user):
			return Response('Not enrolled yet!', status=status.HTTP_403_FORBIDDEN)
		return super().create(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		return self.perform_change(request, 'update', *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		return self.perform_change(request, 'destroy', *args, **kwargs)

	def perform_change(self, request, action, *args, **kwargs):
		user = request.user
		comment = self.get_object()
		if not comment.is_owner(user):
			return Response('you do not have permission to change this comment.',
							 status=status.HTTP_403_FORBIDDEN)
		if action == 'update':
			return super().update(request, *args, **kwargs)
		return super().destroy(request, *args, **kwargs)


	# def get_serializer_class(self):
	# 	serializer_map = {
    #         'reply': ReplySerializer,
    #     }
	# 	return serializer_map.get(self.action, CommentSerializer)

	# @action(detail=True, methods=['put', 'delete'],
	# permission_classes=[IsInstructor], url_path='reply/(?P<rid>[^/.]+)')
	# def reply(self, request, rid, *args, **kwargs):
	# 	instructor = request.user.instructor
	# 	comment = self.get_object()
	# 	if comment.is_course_owner(instructor):
	# 		self.kwargs['pk'] = rid
	# 		if request.method == 'PUT':
	# 			return self.update(request, *args, **kwargs)
	# 		return self.destroy(request, *args, **kwargs)
	# 	return Response('you are not the course owner.', 
	# 						status=status.HTTP_403_FORBIDDEN)



class ReplytViewSet(ModelViewSet):
	queryset = Comment.objects.select_related('parent').all()
	serializer_class = ReplySerializer
	permission_classes = [IsInstructor]
	http_method_names = ['post', 'put', 'delete']

	def get_queryset(self):
		return Comment.objects.filter(
			Q(course_id=self.kwargs.get('course_pk'))&~Q(parent=None))
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['course'] = self.kwargs.get('course_pk')
		context['parent'] = self.kwargs.get('parent_pk')
		return context

	def create(self, request, *args, **kwargs):
		return self.perform_action(request, 'create', *args, **kwargs)

	def update(self, request, *args, **kwargs):
		return self.perform_action(request, 'update', *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		return self.perform_action(request, 'destroy', *args, **kwargs)

	def perform_action(self, request, action, *args, **kwargs):
		instructor = request.user.instructor
		comment = get_object_or_404(Comment.objects, pk=self.kwargs.get('parent_pk'))
		if not comment.is_course_owner(instructor):
			return Response('you are not the course owner.',
							 status=status.HTTP_403_FORBIDDEN)
		if action == 'create':
			return super().create(request, *args, **kwargs)
		if action == 'update':
			return super().update(request, *args, **kwargs)
		return super().destroy(request, *args, **kwargs)

