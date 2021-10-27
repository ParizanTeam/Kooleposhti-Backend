from django.db import models
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    class Meta:
        # model = User
        # fields = ['username', 'email', 'phone_no', 'password1', 'password2']
        permissions = [  # auth_permission (codename, name)
            ('cancel_order', 'Can cancel order')
        ]

class Verification(models.Model):

    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)


class Instructor(models.Model):
    '''
    fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True, default=None)
    # phone = models.CharField(max_length=11)
    birth_date = models.DateField(null=True)  # nullable

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # class Meta:
    #     odering = ['user__first_name', 'user__last_name']


class Student(models.Model):
    '''
    fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True, default=None)
    # phone = models.CharField(max_length=11)
    birth_date = models.DateField(null=True)  # nullable

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
