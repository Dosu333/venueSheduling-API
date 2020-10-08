from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import Department, Role

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email','password','first_name','last_name','department')
        extra_kwargs = {'password': {'write_only':True, 'min_length':8}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting password correctly and returnng it"""
        password = validated_data.pop('password',None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializes department model object"""

    class Meta:
        model = Department
        fields = ('__all__')
        read_only_fields = ['id',]

class RoleSerializer(serializers.ModelSerializer):
    """Serializes department model object"""

    class Meta:
        model = Role
        fields = ('__all__')
        read_only_fields = ['id',]