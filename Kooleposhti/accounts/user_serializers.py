from rest_framework import serializers
from rest_framework.utils import model_meta
from .models import User
from rest_framework import serializers
from .serializers import update_relation


class BaseUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user.username')
    email = serializers.EmailField(read_only=True, source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_no = serializers.CharField(source='user.phone_no')
    birth_date = serializers.DateField(source='user.birth_date')
    roles = serializers.ReadOnlyField(source='user.get_user_roles')

    class Meta:
        ref_name = None
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'phone_no', 'birth_date',
                  'roles', ]

    def update(self, instance, validated_data):
        update_relation(instance, validated_data, 'user')
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


class UserSerializer(BaseUserSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_no = serializers.CharField()
    birth_date = serializers.DateField()
    roles = serializers.ReadOnlyField(source='get_user_roles')

    class Meta (BaseUserSerializer.Meta):
        model = User
        fields = BaseUserSerializer.Meta.fields
