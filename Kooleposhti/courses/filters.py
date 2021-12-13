
from django_filters.rest_framework import FilterSet
from .models import Course, Category
import django_filters




class CourseFilter(FilterSet):
    age_lte = django_filters.NumberFilter(field_name="max_age", lookup_expr='lte')
    age_gte = django_filters.NumberFilter(field_name="min_age", lookup_expr='gte')
    # mm = django_filters.LookupChoiceFilter(field_name="categories")
    class Meta:
        model = Course
        # fields = ['mm']
        fields = ['age_lte', 'age_gte']
        fields = {
            # 'instructor_id': ['exact'],
            'categories': ['contains'],
            'price': ['gt', 'lt'],
            'start_date': ['gt', 'lt'],   
            # 'max_age': ['gte'],
            # 'min_age': ['lte'],
        }
