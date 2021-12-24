from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import *
from decimal import Decimal
from accounts.models import Instructor
from images.serializers import CommentImageSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from accounts.serializers.instructor_serializer import InstructorSerializer
import jdatetime
import jalali_date
from datetime import date, datetime, time, timedelta
import base64
import os
from rest_framework.exceptions import ValidationError

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['course', 'name']
        extra_kwargs = {'course': {'write_only': True}}


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['course', 'text']
        extra_kwargs = {'course': {'write_only': True}}


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['date', 'day', 'month', 'week_day', 'start_time', 'end_time']
        read_only_fields = ['day', 'month', 'week_day', 'end_time']

    def create(self, validated_data):
        # course = validated_data.pop('course')
        course_pk = self.context['course']
        course = Course.objects.get(pk=course_pk)
        date = validated_data['date']
        new_time = datetime.combine(
            date.today(), validated_data['start_time']) + timedelta(minutes=course.duration)
        end_time = new_time.time()
        day = date.day
        month = Session.MonthNames[date.month - 1][1]
        week = jdatetime.date(date.year, date.month, date.day).weekday()
        week_day = Session.WeekNames[week][1]
        return Session.objects.create(course=course, day=day, month=month,
                                      week_day=week_day, end_time=end_time, **validated_data)



class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["id", "course", "title", "number", "question", "created_date",
                "start_date", "start_time", "end_date", "end_time"]
        read_only_fields = ['created_date', 'number']

    def create(self, validated_data):
        course = validated_data.get('course', None)
        validated_data['number'] = len(course.assignments.all()) + 1
        end_date = validated_data['end_date']
        end_time = validated_data['end_time']
        validated_data['date'] = jdatetime.datetime(
            end_date.year, end_date.month, end_date.day, hour=end_time.hour, 
            minute=end_time.minute, second=end_time.second).togregorian()
        return super().create(validated_data)


# class StudentHomeworkSerializer(serializers.ModelSerializer):
#     image =HomeworkImageSerializer(
#         source='user.image', read_only=True)
#     class Meta:
#         model = Student
#         fields = ['id', 'first_name', 'last_name', 'image',]


class CourseTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'title']


class AssignmentStudentSerializer(serializers.ModelSerializer):
    course = CourseTitleSerializer(read_only=True)
    class Meta:
        model = Assignment
        fields = ["id", "course", "title", "end_date", "end_time"]


class HomeworkSerializer(serializers.ModelSerializer):
    # feedback = FeedbackSerializer(read_only=True)
    # student = StudentHomeworkSerializer(read_only=True)
    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ['assignment', 'submited_date', 'grade']

    def create(self, validated_data):
        assignment = self.context['assignment']
        return Homework.objects.create(
                    assignment_id=assignment, **validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['created_date', 'last_update', 'homework']

    def create(self, validated_data):
        homework = self.context['homework']
        return Feedback.objects.create(
                        homework_id=homework, **validated_data)


class UserCommentSerializer(serializers.ModelSerializer):
    image = CommentImageSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'image']


class ReplySerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'created_date', 'text', 'user']
        read_only_fields = ['id', 'created_date', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['course_id'] = self.context.get("course")
        validated_data['parent_id'] = self.context.get("parent")
        validated_data['created_date'] = jdatetime.datetime.now().__str__()
        validated_data['user'] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(read_only=True)
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'created_date', 'text', 'user', 'reply']
        read_only_fields = ['id', 'created_date']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['course_id'] = self.context.get("course")
        validated_data['created_date'] = jdatetime.datetime.now().__str__()
        validated_data['user'] = request.user
        return super().create(validated_data)


# class CommentReplySerializer(serializers.ModelSerializer):
#     reply = ReplySerializer(read_only=True)
#     comment = CommentSerializer(read_only=True)
#     class Meta:
#         model = Comment
#         fields = ['comment', 'reply']
#         read_only_fields = ['comment', 'reply']

class InstructorCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'image', 'start_date',
                  'end_date', 'max_students']


class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    goals = GoalSerializer(many=True, read_only=True)
    sessions = SessionSerializer(many=True, read_only=True)
    # instructor = serializers.HyperlinkedRelatedField(
    #     queryset=Instructor.objects.all(), view_name='instructor-detail')
    class Meta:
        model = Course
        fields = ('id', 'created_at', 'categories', 'instructor',
                  'duration', 'title', 'image', 'description', 'start_date',
                  'end_date', 'price', 'rate', 'rate_no', 'link', 'min_students', 
                  'max_students', 'capacity', 'min_age', 'max_age',
                  'tags', 'goals', 'sessions')
        read_only_fields = ('id', 'created_at', 'instructor', 'link', 
                            'rate', 'rate_no', 'capacity')
    
        new_price = serializers.SerializerMethodField(
            method_name='calculate_new_price')

    def calculate_new_price(self, course: Course):
        return course.price * Decimal(1.1)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['instructor'] = request.user.instructor
        validated_data['capacity'] = validated_data['max_students']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        capacity = instance.capacity + \
            validated_data.get(
                'max_students', instance.max_students) - instance.max_students
        if capacity < 0:
            self.fail("course remaining capacity should not be negative")
        validated_data['capacity'] = capacity
        return super().update(instance, validated_data)



class CategorySerializer(serializers.ModelSerializer):
    # courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'courses']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'date', 'name', 'description')

    def create(self, validated_data):
        course_id = self.context['course_id']
        return Review.objects.create(
            course_id=course_id,
            **validated_data
        )


class SimpleCourseSerializer():
    # Basic info for Cart item
    class Meta:
        model = Course
        fields = ['id', 'title', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    course = SimpleCourseSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.course.price

    class Meta:
        model = CartItem
        fields = ['id', 'course', 'quantity', 'total_price']


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: ShoppingCart):
        return sum([item.quantity*item.course.price for item in cart.items.all()])

    class Meta:
        model = ShoppingCart
        fields = ['id', 'items', 'total_price']


class DiscountSerializer(serializers.ModelSerializer):
    default_error_messages = {'code_exists': 'Duplicate: The code already exists'}
    code=serializers.CharField(max_length=255,required=False)
    class Meta:
        model = Discount
        fields = ['discount','expiration_date','title','code','used_no','created_date']
        read_only_fields=['used_no','created_date']


    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['owner'] = request.user.instructor
        return super().create(validated_data)

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)
        errors = {}
        is_code_exist=Discount.objects.filter(code=validated_attrs['code']).exists()
        if (is_code_exist):
            errors['code'] = self.error_messages['code_exists']

        if errors:
            raise ValidationError(errors)

        return validated_attrs


