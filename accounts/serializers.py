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
    phone = serializers.CharField(validators = [validate_phone])
    password = serializers.CharField(write_only=True)


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user', 'id']


class UserEditSerializer(serializers.ModelSerializer):
    profile = ProfileEditSerializer(many=False)
    class Meta:
        model = CustomUser
        fields = ('email', 'image', 'first_name', 'last_name', 'profile')
    
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


class UserRetriveSerializer(serializers.ModelSerializer):
    profile = ProfileEditSerializer(many=False)
    class Meta:
        model = CustomUser
        fields = ('email', 'image', 'first_name', 'last_name', 'profile')

