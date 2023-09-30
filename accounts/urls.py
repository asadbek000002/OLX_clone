from django.urls import path

from .views import UserRegisterView, UserEditAPIView, UserRetrieveAPIView, UserDetailAPIView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='auth_register'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/', UserEditAPIView.as_view(), name='user_update'),
    path('edit/', UserEditAPIView.as_view(), name='edit'),
    path('profile/<pk>/', UserDetailAPIView.as_view(), name='detail'),
    
]