from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from .models import Department

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    class Meta:
        model = get_user_model()
        fields = ('email','first_name','last_name','department','password')
        extra_kwargs = {'password': {'write_only':True, 'min_length':8}}

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation['department'] = Department.objects.get(id=str(representation['department'])).name
        return representation

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

class AdminManageUserSerializer(serializers.ModelSerializer):
    """Serializes role field of user model"""
    department = serializers.StringRelatedField()
    class Meta:
        model = get_user_model()
        fields = ('groups','is_staff','id','email','first_name','last_name','department')
        read_only_fields  = ['email','first_name','last_name','department']

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        str_group = []
        for id in representation['groups']:
            role = Group.objects.get(pk=id).name
            str_group.append((id,role))
        representation['groups'] = str_group
        return representation

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('__all__')

    def to_representation(self,instance):
        representation = super().to_representation(instance)
        str_perm = []
        for id in representation['permissions']:
            role = Permission.objects.get(pk=id).name
            str_perm.append(role)
        representation['permissions'] = str_perm
        return representation
