from django.urls import path
from .views import AddressDetail, SocialnetworkDetail, FaqsList

urlpatterns = [
    path('address/<int:id>/', AddressDetail.as_view(), name='address_detail'),
    path('social/<int:id>/', SocialnetworkDetail.as_view(), name='social_detail'),
    path('faqs/list/', FaqsList.as_view(), name='faqs_list')
]