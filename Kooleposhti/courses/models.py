from django.db import models
from accounts.models import Instructor, Student
from uuid import uuid4
from Kooleposhti import settings


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    # course_set -> all courses promotions applied to
    discount = models.FloatField()

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    '''
    ('title', 'description', 'price', 'last_update', 'instructor')
    '''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # 9999.99
    # first time we create Course django stores the current datetime
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    enrollment_start_date = models.DateTimeField()
    enrollment_end_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    start_class = models.DateTimeField()
    end_class = models.DateTimeField()
    promotions = models.ManyToManyField(Promotion)
    max_students = models.IntegerField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    def __str__(self):
        return self.title



class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Order (models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)


class OrderItem (models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)


class ShoppingCart(models.Model):  # Cart
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, related_name='items')  # ShoppingCart.items
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [
            ['cart', 'course'],
        ]


class Review(models.Model):
    '''
    fields = ('id', 'date', 'name', 'description', 'course')
    '''
    course = models.ForeignKey(
        Instructor, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
