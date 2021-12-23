from django.core.validators import MinValueValidator, MaxValueValidator
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
    '''
    instructor, student, userskyroom, publicprofile
    '''
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=11, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(null=True)
    # image = models.OneToOneField(MyImage, on_delete=models.CASCADE, null=True)
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


class UserSkyRoom(models.Model):
    skyroom_id = models.BigIntegerField(
        primary_key=True, verbose_name='SkyRoom ID')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Verification(models.Model):
    email = models.EmailField(primary_key=True)
    token = models.CharField(max_length=6)
    create_time = models.DateTimeField(auto_now_add=True)


class Tag (models.Model):
    name = models.CharField(max_length=255, null=False,
                            blank=False, unique=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    '''
    fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    rate = models.IntegerField(null=True, validators=[
                               MinValueValidator(0), MaxValueValidator(5)])
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
    age = models.IntegerField(null=True, validators=[
                              MinValueValidator(0), MaxValueValidator(18)])
    # phone = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name


class PublicProfile(models.Model):
    '''
    location, bio, rate
    '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Wallet(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(default=0, blank=True, decimal_places=3, max_digits=12)
    card_no = models.CharField(blank=True, null=True, max_length=16)
    sheba = models.CharField(blank=True, null=True, max_length=24)

    def __str__(self):
        return f"{self.user.username} {self.balance}"
    
    def is_set(self):
        return self.card_no and self.sheba

    def withdraw(self, amount):
        self.balance -= amount
        self.save()
    
