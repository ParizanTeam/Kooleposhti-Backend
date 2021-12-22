from django.db import models
from accounts.models import Instructor, Student, User
from uuid import uuid4
from Kooleposhti import settings


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    # course_set -> all courses promotions applied to
    discount = models.FloatField()


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    image = models.ImageField(
        upload_to='images/course_images/', blank=True, null=True)

    def __str__(self):
        return self.title


class Course(models.Model):
    '''
    ('title', 'description', 'price', 'last_update', 'instructor')
    '''
    room_id = models.IntegerField(unique=True, blank=True, null=True)
    instructor = models.ForeignKey(
        Instructor, blank=True, related_name='courses', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='courses')
    students = models.ManyToManyField(
        Student, blank=True, related_name='courses')
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True)
    image = models.ImageField(
        upload_to='images/course_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)  # 9999.99
    rate = models.DecimalField(
        max_digits=2, decimal_places=1, default=5, blank=True)
    rate_no = models.IntegerField(default=0, blank=True)
    # first time we create Course django stores the current datetime
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    duration = models.IntegerField()
    promotions = models.ManyToManyField(Promotion, blank=True)
    min_students = models.IntegerField(blank=True, default=1)
    max_students = models.IntegerField()
    capacity = models.IntegerField(blank=True)
    min_age = models.IntegerField(default=1)
    max_age = models.IntegerField(default=18)
    link = models.URLField(blank=True)
    # links_credit_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def is_enrolled(self, user):
        return self.students.filter(id=user.id).exists()

    def is_owner(self, user):
        return self.instructor == user

    def is_course_user(self, user):
        return (user.has_role('student') and self.is_enrolled(user.student)) \
		or (user.has_role('instructor') and self.is_owner(user.instructor))

    def update_rate(self):
        rates = self.rates.all()
        self.rate_no = len(rates)
        self.rate = round(sum([rate_obj.rate for rate_obj in rates]) / self.rate_no, 1)
        self.save()

    def update_capacity(self):
        self.capacity = self.max_students - len(self.students.all())
        self.save()
        
    def can_enroll(self, student):
        return True


# class Link(models.Model):
#     course = models.ForeignKey(
#         Course, on_delete=models.CASCADE, related_name='links')
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, related_name='links')
#     url = models.URLField()
#     def __str__(self):
#         return f"{self.course.title} {self.student.user.username}"

class Rate(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='rates')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='rates')
    rate = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    def __str__(self):
        return f"{self.course.title} {self.rate}"


class Session(models.Model):

    WeekNames = [
        ('0', "شنبه"),
        ('1', "یکشنبه"),
        ('2', "دو‌شنبه"),
        ('3', "سه‌شنبه"),
        ('4', "چها‌ر‌شنبه"),
        ('5', "پنجشنبه"),
        ('6', "جمعه")
    ]
    MonthNames = [
        ('1', "فروردین"),
        ('2', "اردیبهشت"),
        ('3', "خرداد"),
        ('4', "تیر"),
        ('5', "مرداد"),
        ('6', "شهریور"),
        ('7', "مهر"),
        ('8', "آبان"),
        ('9', "آذر"),
        ('10', "دی"),
        ('11', "بهمن"),
        ('12', "اسفند")
    ]

    course = models.ForeignKey(
        Course, blank=True, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    day = models.IntegerField(blank=True)
    month = models.CharField(max_length=10, blank=True, choices=MonthNames)
    week_day = models.CharField(max_length=10, blank=True, choices=WeekNames)
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True)

    def __str__(self):
        return f"{self.course.title} {self.date} {self.start_time}-{self.end_time}"


class Comment(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    parent = models.OneToOneField('Comment', on_delete=models.CASCADE, 
                        related_name='reply', null=True, blank=True)
    created_date = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return f"{self.course.title} {self.text}"

    def is_owner(self, user):
        return self.user == user

    def is_course_owner(self, user):
        return self.course.instructor == user


class Tag(models.Model):
    course = models.ForeignKey(
        Course, blank=True, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course.title} {self.name}"


class Assignment(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    number = models.IntegerField(blank=True)
    question = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    date = models.DateTimeField(blank=True)

    def __str__(self):
        return f"{self.course.title} {self.title}"

    def is_course_owner(self, user):
        return self.course.instructor == user

    def is_course_student(self, user):
        return self.course.is_enrolled(user)

    def is_course_user(self, user):
        return (user.has_role('student') and self.is_course_student(user.student)) \
		or (user.has_role('instructor') and self.is_course_owner(user.instructor))

    def sent(self, user):
        return self.homeworks.filter(student=user).exists()

class Homework(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='homeworks')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='homeworks')
    submited_date = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"{self.assignment.course.title}  \
            {self.assignment.title} {self.student.user.username}"

    def is_owner(self, user):
        return self.student == user

    def is_course_owner(self, user):
        return self.assignment.course.instructor == user

    def can_see(self, user):
        return (user.has_role('student') and self.is_owner(user.student)) \
		or (user.has_role('instructor') and self.is_course_owner(user.instructor))



class Feedback(models.Model):
    grade_choices = [
        ('عالی', "A"),
        ("خیلی خوب", "B"),
        ("خوب", "C"),
        ("نیاز به تلاش بیشتر", "D"),
    ]
    homework = models.OneToOneField(
        Homework, on_delete=models.CASCADE, related_name='feedback')
    description = models.TextField(blank=True, null=True)
    grade = models.CharField(choices=grade_choices, max_length=18)
    last_update = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def is_mine(self, user):
        return self.homework.student == user

    def is_course_owner(self, user):
        return self.homework.assignment.course.instructor == user

    def can_see(self, user):
        return (user.has_role('student') and self.is_mine(user.student)) \
		or (user.has_role('instructor') and self.is_owner(user.instructor))


class Goal(models.Model):
    course = models.ForeignKey(
        Course, blank=True, related_name='goals', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.course.title} {self.text}"



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
