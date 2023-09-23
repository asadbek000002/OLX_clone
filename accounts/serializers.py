from uuid import uuid4

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser, Profile 
from .services import  validate_phone

# from django.shortcuts import get_object_or_404
# from django.contrib.auth import authenticate
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
# from django.db.models import Q

class RegisterSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(validators = [validate_phone])
    is_staff = serializers.BooleanField(default=False)


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user', 'id']


class UserEditSerializer(serializers.ModelSerializer):
    profile = ProfileEditSerializer(many=False)
    class Meta:
        model = CustomUser
        exclude = [
            'is_staff', 'is_active', 'date_joined', 'custom_id', 
            'is_worker', 'is_company', 'is_deleted', 'password',
            'is_superuser', 'groups', 'user_permissions'
        ]
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            # user = self.data['user']
            profile_db = Profile.objects.get(user=instance)
            print(profile_db)
            profile_serializer = ProfileEditSerializer(data=profile_data, partial=True)
            if profile_serializer.is_valid():
                profile_serializer.update(profile_db, profile_data)
        return instance


