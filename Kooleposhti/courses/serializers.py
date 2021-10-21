from rest_framework import serializers
from .models import Course, Review
from decimal import Decimal
from accounts.models import Instructor


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
