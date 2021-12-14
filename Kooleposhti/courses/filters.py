
from django_filters.rest_framework import FilterSet
from .models import Course, Category
import django_filters




class CourseFilter(FilterSet):
    age_lte = django_filters.NumberFilter(field_name="max_age", lookup_expr='lte')
    age_gte = django_filters.NumberFilter(field_name="min_age", lookup_expr='gte')
    # week_day = django_filters.CharFilter(field_name="sessions__week_day")
    # mm = django_filters.LookupChoiceFilter(field_name="categories")
    class Meta:
        model = Course
        # fields = ['mm']
        fields = ['age_lte', 'age_gte']
        fields = {
            # 'instructor_id': ['exact'],
            'categories': ['exact'],
            # 'sessions__week_day': ['exact'],
            'price': ['gte', 'lte'],
            'start_date': ['gte', 'lte'],   
            # 'max_age': ['gte'],
            # 'min_age': ['lte'],
        }
