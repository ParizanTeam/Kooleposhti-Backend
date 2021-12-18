from rest_framework.response import Response
from accounts.permissions import *
from ..models import *
from ..serializers import *
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny




class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(course_id=self.kwargs.get('course_pk'))
