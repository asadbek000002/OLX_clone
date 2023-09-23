from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import City, District, Product
from .serializers  import ProductSerializer

from .models import Category


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

class ProductViewSet(generics.ListAPIView):
    queryset = Product.objects.filter(is_deleted=False, is_active=True)
    serializer_class = ProductSerializer

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





