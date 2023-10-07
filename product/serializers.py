from rest_framework import serializers
from .models import City, District, Kino

from .models import Category, Product, Saved, Comment, Ban, Banned
from accounts.serializers import (
    ProductUserRetriveSerializer,
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'parent')
        extra_kwargs = {
            'user': {'read_only': True, 'required': False},
        }


class ProductSerializer(serializers.ModelSerializer):
    user = ProductUserRetriveSerializer(many=False)
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'slug': {'read_only': True, 'required': False},
            'user': {'read_only': True, 'required': False},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('product', 'body')


class SavedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saved
        fields = ('id', 'user', 'product', 'created_at')
        extra_kwargs = {
            'id': {'read_only': True,'required': False},
            'user': {'read_only': True,'required': False},
            'created_at': {'read_only': True,'required': False},
        }


class SavedListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Saved
        fields = ('id', 'user', 'product', 'created_at')
        extra_kwargs = {
            'id': {'read_only': True, 'required': False},
            'user': {'read_only': True, 'required': False},
            'created_at': {'read_only': True, 'required': False},
        }


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class BanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ban
        fields = "__all__"


class BanedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banned
        fields = ['comment', 'ban', 'product']
        

class KinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kino
        fields = ['name', 'url']
        


