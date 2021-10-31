from django.contrib.auth.backends import BaseBackend, UserModel, ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Exists, OuterRef, Q
import rest_framework_simplejwt.serializers
from pprint import pprint


class MyModelBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        username = None if username == '' else username
        email = None if email == '' else email

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if (email is None and username is None) or password is None:
            return
        try:
            if not username is None:
                user = UserModel._default_manager.get_by_natural_key(username)
            elif not email is None:
                user = UserModel._default_manager.get(
                    email=request.data['email'])
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
