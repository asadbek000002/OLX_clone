from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions

from accounts.models import CustomUser

from .models import Category, City, District, Product, Saved, Comment, Ban, Banned

from .serializers import ProductSerializer, SavedSerializer, CitySerializer,\
                          DistrictSerializer, CommentSerializer, CommentCreateSerializer, BanSerializer, BanedSerializer
from .serializers import CategorySerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=False).prefetch_related('childs', 'childs__childs')
    serializer_class = CategorySerializer
    
    

    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        
        filter_kwargs = {'parent': self.kwargs[lookup_url_kwarg]}
        
        queryset = queryset.filter(**filter_kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Pagination 
class ProductPagination(PageNumberPagination):
    page_size=2
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'showing_count': self.page_size,
            'results': data
        })

    
class ProductViewSet(generics.ListAPIView):
    
    queryset = Product.objects.filter(is_deleted=False, is_active=True).order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = ProductPagination 

    

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_deleted=False, is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        post_tags_ids = instance.tags.values_list('id', flat=True)
        similar_posts = self.queryset.filter(tags__in=post_tags_ids, category=instance.category).exclude(id=instance.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:10]
        serializer1 = self.get_serializer(similar_posts, many=True)
        return Response({"detail": serializer.data, "same_prods": serializer1.data})
    

class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_authenticated:
            if instance.user == self.request.user:
                instance.is_deleted = True
                instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if self.request.user.is_authenticated:
            if instance.user ==self.request.user:
                serializer = self.get_serializer(instance, data=request.data, partial=partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return Response(serializer.data)

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_400_BAD_REQUEST)



class CommentList(generics.ListAPIView):
    queryset = Comment.objects.filter(is_active=True, is_banned=False)
    serializer_class = CommentSerializer

    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        
        queryset = queryset.filter(**filter_kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    
    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class CityViewSet(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    

class DistrictViewSet(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        
        queryset = self.queryset


        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        
        queryset = queryset.filter(**filter_kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SavedListView(generics.ListAPIView):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer


class SavedDeleteView(generics.DestroyAPIView):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_authenticated:
            if instance.user == self.request.user:
                instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SavedAPIView(generics.CreateAPIView):
    serializer_class = SavedSerializer

    def post(self, request):
        data = request.data

        product = Product.objects.all(user=request.user)
        data['product'] = product.pk
        serializer = SavedSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class BanViewList(generics.ListAPIView):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer
    # permission_classes = [permissions.IsAuthenticated]


class BanCreate(generics.CreateAPIView):
    queryset = Banned.objects.all()
    serializer_class = BanedSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)
            validated_data = serializer.validated_data.get('product')
            product_id = validated_data
            ban_count = Ban.objects.filter(product__id=product_id).count()
            if ban_count >= 10:
                product = Product.objects.get(id=product_id)
                product.is_banned = True
                product.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_400_BAD_REQUEST)



