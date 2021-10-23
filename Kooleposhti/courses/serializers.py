from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import CartItem, Course, Review, ShoppingCart
from decimal import Decimal
from accounts.models import Instructor
from djoser.serializers import UserSerializer as BaseUserSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title', 'description', 'price',
                  'last_update', 'instructor', 'new_price')  # __all__
    instructor = serializers.HyperlinkedRelatedField(
        queryset=Instructor.objects.all(), view_name='instructor-detail')
    new_price = serializers.SerializerMethodField(
        method_name='calculate_new_price')

    def calculate_new_price(self, course: Course):
        return course.price * Decimal(1.1)


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



class UserSerializer(BaseUserSerializer):
    #  'current_user': 'djoser.serializers.UserSerializer',
    class Meta (BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
