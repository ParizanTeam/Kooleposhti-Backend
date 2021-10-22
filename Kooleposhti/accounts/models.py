from django.db import models
from django import forms
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=11)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    class Meta:
        # model = User
        # fields = ['username', 'email', 'phone_no', 'password1', 'password2']
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class Instructor(models.Model):
    '''
    fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
    '''
    # user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default=None)
    phone = models.CharField(max_length=11)
    birth_date = models.DateField(null=True)  # nullable

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # class Meta:
    #     odering = ['user__first_name', 'user__last_name']


class Student(models.Model):
    '''
    fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
    '''
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, default=None)
    phone = models.CharField(max_length=11)
    birth_date = models.DateField(null=True)  # nullable
