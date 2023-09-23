from django.urls import include, path

from .views import * 


app_name = "categories"

urlpatterns = [
    path('category/', CategoryList.as_view()),
    path('category/sub-category/<pk>/', CategoryListAPIView.as_view()),
    path('product-create',ProductCreateAPIView.as_view() ),
    path('product-list/',ProductViewSet.as_view() ),
    path('product-delete/<int:id>/', ProductDestroyAPIView.as_view()),
    path('product-update/<pk>/', ProductUpdateAPIView.as_view()),
    path('saved/', SavedAPIView.as_view(), name='saved'),
    path('delete/<int:id>/', SavedDeleteView.as_view(), name='delete'),
    path('list/', SavedListView.as_view (), name='list'),
    
]