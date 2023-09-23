from rest_framework import serializers

from .models import Category, Product, Saved, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'parent')
        extra_kwargs = {
            'user': {'read_only': True, 'required': False},
        }
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

        
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

