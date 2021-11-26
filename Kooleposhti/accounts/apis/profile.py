from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from accounts.apis.my_views import MyGenericViewSet
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, permission_classes
from rest_framework import status
from accounts.models import User
from accounts.permissions import IsInstructor, IsStudent
from accounts.serializers.public_profile import BasePublicProfileSerializer, InstructorPublicProfileSerializer, StudentPublicProfileSerializer
from rest_framework import mixins


class PublicProfile (MyGenericViewSet):
    queryset = User.objects.all()
    # serializer_class =

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class(
            instance=kwargs.get('instance'))
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self, *args, **kwargs):
        instance = kwargs.get('instance')
        serializer_class = BasePublicProfileSerializer
        if self.action == 'get_user_profile' or \
                self.action == 'update_user_profile':
            if instance is None:
                return serializer_class
            if instance.has_role('student'):
                serializer_class = StudentPublicProfileSerializer
            elif instance.has_role('instructor'):
                serializer_class = InstructorPublicProfileSerializer
        elif self.action == 'list':
            serializer_class = BasePublicProfileSerializer
        return serializer_class

    """
    Update a model instance.
    """
    @action(detail=False, methods=['PUT', 'GET', ], url_path='update-profile')
    def update_user_profile(self, request, *args, **kwargs):
        instance = request.user
        if request.method == 'PATCH':
            kwargs['partial'] = True
        if request.method == 'PUT':
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(
                instance=instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        elif request.method == 'GET':
            serializer = self.get_serializer(instance=instance)
            return Response(
                data={
                    "data": serializer.data,
                    "message": "Profile fetched successfully"
                }, status=status.HTTP_200_OK
            )

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['GET', ], url_path='public/(?P<username>[^/.]+)')
    def get_user_profile(self, request, username=None):
        if username is None:
            return Response({'error': 'username is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(self.get_queryset(), username=username)
        serializer = self.get_serializer(instance=user)
        return Response(
            data={
                'data': serializer.data,
                'message': 'success'
            }, status=status.HTTP_200_OK
        )

    def get_permissions(self):
        permissions_map = {
            'list': [IsAdminUser, ],
            'update_user_profile': [IsAuthenticated, ],
            'get_user_profile': [AllowAny, ],

        }
        return permissions_map.get(self.action, [IsAdminUser, ])

    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
