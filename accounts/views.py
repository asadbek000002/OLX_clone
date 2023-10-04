from django.shortcuts import render
from .models import CustomUser, Profile
from uuid import uuid4
from .serializers import RegisterSerializer, UserEditSerializer, UserRetriveSerializer, UserSerializer
from rest_framework import (
    generics, 
    permissions,
    response,
    status,
)
from rest_framework.response import Response

# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = CustomUser()
        for key, value in serializer.validated_data.items():
            setattr(user, key, value)
        user.set_password(serializer.validated_data['password'])
        user.save()
        Profile.objects.create(user=user)
        



class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.filter(is_active=True, is_deleted=False)
    serializer_class = UserRetriveSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        obj = CustomUser.objects.filter(
            email=self.request.user.email
        ).select_related('profile').first()
        return obj
    


class UserEditAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(is_active=True, is_deleted=False)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserEditSerializer

    def get_object(self):
        return CustomUser.objects.get(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_object(self):
        user_id = self.request.user.id
        return CustomUser.objects.filter(id=self.kwargs['pk']).prefetch_related('profile').first()


