from rest_framework import serializers

from .models import Address, Socialnetwork, Faqs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class SocialnetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socialnetwork
        fields = '__all__'


class FaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = '__all__'