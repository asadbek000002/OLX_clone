from django.shortcuts import render
from rest_framework import generics


from .models import Address, Socialnetwork, Faqs


from .serializers import AddressSerializer, SocialnetworkSerializer, FaqsSerializer

# Create your views here.


class AddressDetail(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class SocialnetworkDetail(generics.ListAPIView):
    queryset = Socialnetwork.objects.all()
    serializer_class = SocialnetworkSerializer


class FaqsList(generics.ListAPIView):
    queryset = Faqs.objects.all()
    serializer_class = FaqsSerializer
