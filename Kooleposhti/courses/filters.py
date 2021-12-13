
from django_filters.rest_framework import FilterSet
from .models import Course, Category
import django_filters




class CourseFilter(FilterSet):
    # min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    # max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    # mm = django_filters.LookupChoiceFilter(field_name="categories")
    class Meta:
        model = Course
        # fields = ['mm']
        fields = {
            # 'instructor_id': ['exact'],
            'categories': ['contains'],
            'price': ['gt', 'lt'],
            'start_date': ['gt', 'lt'],   
            'max_age': ['gt', 'lt']
        }
