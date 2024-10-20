from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    
    class Meta:
        model = User
        fields = ('id', 'lastName', 'firstName', 'username', 'password')
        
class UserNoPSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    
    class Meta:
        model = User
        fields = ('id', 'lastName', 'firstName', 'username')
        
class UserRolesSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    
    roles = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True,
        required=False
    )
    
    class Meta:
        model = User
        fields = ('id', 'lastName', 'firstName', 'username', 'password', 'roles')

    def create(self, validated_data):
        roles = validated_data.pop('roles', ['none'])
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        if not ('none' in roles):
            self.assign_roles(user, roles)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        roles = validated_data.pop('roles', ['none'])
        if not ('none' in roles):
            self.assign_roles(instance, roles)

        instance.save()
        return instance

    def assign_roles(self, user, roles):
        user.is_superuser = 'admin' in roles
        user.is_staff = user.is_superuser
        user.is_doctor = 'doctor' in roles
        user.is_manager = 'manager' in roles
        user.save()
        
class UserUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    
    class Meta:
        model = User
        fields = ('id', 'lastName', 'firstName', 'password')