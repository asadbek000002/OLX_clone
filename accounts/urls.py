from django.urls import path

from .views import UserRegisterView, UserEditAPIView, UserRetrieveAPIView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='auth_register'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('update/', UserEditAPIView.as_view(), name='user_update'),
    
]