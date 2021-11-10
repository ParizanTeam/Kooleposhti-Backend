from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import *
from decimal import Decimal
from accounts.models import Instructor
from djoser.serializers import UserSerializer as BaseUserSerializer
from accounts.serializers import InstructorSerializer
from accounts.student_serializers import StudentSerializer
import jdatetime


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    # def create(self, validated_data):
    #     course_id = self.context.get('course_id')
    #     return Tag.objects.create( course_id=course_id, **validated_data)


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    # def create(self, validated_data):
    #     course_id = self.context.get('course_id')
    #     return Goal.objects.create( course_id=course_id, **validated_data)


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

    # def create(self, validated_data):
    #     course_id = self.context.get('course_id')
    #     return Chapter.objects.create( course_id=course_id, **validated_data)


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

    def create(self, validated_data):
        # course_id = self.context.get('course_id')
        date = validated_data.pop('date')
        date = jdatetime.date(*date.split('/')).togregorian()
        return Class.objects.create(date=date, **validated_data)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request")
        student = request.user
        return Comment.objects.create(student=student, **validated_data)


class CourseSerializer(serializers.ModelSerializer):
    chapter = ChapterSerializer(many=True)
    students = StudentSerializer(many=True)
    tags = TagSerializer(many=True)
    classes = ClassSerializer(many=True)
    instructor = InstructorSerializer()

    class Meta:
        model = Course
        fields = '__all__'
        # fields = ('title', 'description', 'price',
        #           'last_update', 'instructor', 'new_price')  # __all__
    # instructor = serializers.HyperlinkedRelatedField(
    #     queryset=Instructor.objects.all(), view_name='instructor-detail')
    new_price = serializers.SerializerMethodField(
        method_name='calculate_new_price')

    def calculate_new_price(self, course: Course):
        return course.price * Decimal(1.1)

    def create(self, validated_data):
        request = self.context.get("request")
        instructor = request.user
        category = Category.objects.filter(title=validated_data.pop('category'))
        course = Course.objects.create( instructor=instructor, category=category, **validated_data)
        tags = validated_data.pop('tags')
        for tag in tags:
            Tag.objects.create(course=course, **tag)
        goals = validated_data.pop('goals')
        for goal in goals:
            Goal.objects.create(course=course, **goal)
        # chapters = validated_data.pop('chapters')
        # for chapter in chapters:
        #     Chapter.objects.create(course=course, **chapter)
        classes = validated_data.pop('classes')
        for myclass in classes:
            Class.objects.create(course=course, **myclass)
        
        return course




class CategorySerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


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
