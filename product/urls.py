from django.urls import path

from .views import * 


app_name = "categories"

urlpatterns = [
    path('category/', CategoryList.as_view()),
    path('category/sub-category/<pk>/', CategoryListAPIView.as_view()),
    path('product-create/', ProductCreateAPIView.as_view()),
    path('product-list/', ProductViewSet.as_view()),
    path('product-detail/<pk>/', ProductDetailAPIView.as_view()),
    path('product-list/', ProductViewSet.as_view()),
    path('product-user-list/', ProductUserListAPIView.as_view()),
    path('product-delete/<pk>/', ProductDestroyAPIView.as_view()),
    path('product-delete/<pk>/', ProductDestroyAPIView.as_view()),
    path('product-update/<pk>/', ProductUpdateAPIView.as_view()),
    path('by/category/<pk>/', ProductByCategory.as_view()),
    path('cities/', CityViewSet.as_view(), name='cities'),
    path('district/<pk>/', DistrictViewSet.as_view(), name='districts'),
    path('comment/<pk>/', CommentList.as_view()),
    path('comment-create/<pk>/', CommentCreateAPIView.as_view()),
    path('saved/', SavedAPIView.as_view(), name='saved'),
    path('saved/delete/<pk>/', SavedDeleteView.as_view(), name='delete'),
    path('saved/list/', SavedListView.as_view(), name='list'),
    path('ban-list/', BanViewList.as_view()),
    path('ban-add/', BanCreate.as_view()),

    # kino
    path('kino-list/', KinoListAPIView.as_view()),
    path('kino-create/', KinoCreateAPIView.as_view()),
    path('kino-detail/<pk>/', KinoDetailAPIView.as_view()),
]



