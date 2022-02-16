from accounts.models import PublicProfile, User
from rest_framework import serializers
from images.serializers import ProfileImageSerializer
from courses.serializers import CourseSerializer
from accounts.serializers.serializers import update_relation
from rest_framework.utils import model_meta


class BasePublicProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(
        source='publicprofile.bio', required=False, allow_null=True, allow_blank=True)
    image = ProfileImageSerializer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'image']
        read_only_fields = ['first_name', 'last_name', 'username', 'image']

    def update(self, instance, validated_data):
        if 'publicprofile' in validated_data:
            if not hasattr(instance, 'publicprofile'):
                instance.publicprofile = PublicProfile.objects.create(
                    user=instance)
                instance.publicprofile.save()
                instance.save()
            update_relation(instance, validated_data, 'publicprofile')
        info = model_meta.get_field_info(instance)
        instance.save()
        return instance


class StudentPublicProfileSerializer(BasePublicProfileSerializer):
    age = serializers.IntegerField(
        source='student.age', min_value=0, max_value=18, required=False, read_only=False)

    class Meta (BasePublicProfileSerializer.Meta):
        # fields = BasePublicProfileSerializer.Meta.fields + ['age']
        fields = ['first_name', 'last_name', 'username', 'bio', 'image', 'age']
        read_only_fields = BasePublicProfileSerializer.Meta.read_only_fields

    def update(self, instance, validated_data):
        if 'student' in validated_data:
            update_relation(instance, validated_data, 'student')
        return super().update(instance, validated_data)


class InstructorPublicProfileSerializer(BasePublicProfileSerializer):
    rate = serializers.DecimalField(
        source='instructor.rate', decimal_places=1, max_digits=2, min_value=0, 
                                max_value=5, required=False, read_only=True)
    courses = CourseSerializer(
        source='instructor.courses', many=True, required=False, read_only=True)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta (BasePublicProfileSerializer.Meta):
        fields = BasePublicProfileSerializer.Meta.fields + ['rate', 'courses']
        read_only_fields = BasePublicProfileSerializer.Meta.read_only_fields + \
            ['rate', 'courses']
