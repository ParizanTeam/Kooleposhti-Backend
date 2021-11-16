from django.db import models
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.conf import settings

from images.models import MyImage

ROLES = [
    'instructor',
    'student',
]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=11, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    image = models.OneToOneField(MyImage, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=255, null=True)

    class Meta:
        # model = User
        # fields = ['username', 'email', 'phone_no', 'password1', 'password2']
        permissions = [  # auth_permission (codename, name)
            ('cancel_order', 'Can cancel order')
        ]

    def has_role(self, role):
        return hasattr(self, role)

    @property
    def get_user_roles(self):
        roles = []
        for role in ROLES:
            if hasattr(self, role):
                roles.append(role)
        return roles


class Verification(models.Model):
    email = models.EmailField(primary_key=True)
    token = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)


class Tag (models.Model):
    name = models.CharField(max_length=255, null=False,
                            blank=False, unique=True)

    def __str__(self) -> str:
        return self.name


class Instructor(models.Model):
    '''
    fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    # phone = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # class Meta:
    #     odering = ['user__first_name', 'user__last_name']


# class StudentManager(models.Manager) :


class Student(models.Model):
    '''
    fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # phone = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
