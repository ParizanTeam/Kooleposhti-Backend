from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import html, model_meta, representation
from .models import Instructor, Tag
from rest_framework import serializers


class TagProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class InstructorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user.username')
    email = serializers.EmailField(read_only=True, source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_no = serializers.CharField(source='user.phone_no')
    birth_date = serializers.DateField(source='user.birth_date')
    tags = TagProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Instructor
        fields = ('id', 'user_id', 'username', 'email',
                  'first_name', 'last_name', 'phone_no', 'birth_date', 'tags')

    def update_relation(self, instance, validated_data, relation):
        assert relation in validated_data, 'user not found in validated_data'
        instance = getattr(instance, relation)
        for key, val in validated_data[relation].items():
            setattr(instance, key, val)

    def update(self, instance, validated_data):
        self.update_relation(instance, validated_data, 'user')
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        # m2m_fields = []
        # for attr, value in validated_data.items():
        #     if attr in info.relations and info.relations[attr].to_many:
        #         m2m_fields.append((attr, value))
        #     else:
        #         setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        # for attr, value in m2m_fields:
        #     field = getattr(instance, attr)
        #     field.set(value)

        return instance