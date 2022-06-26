from django.urls import path
from .import views

urlpatterns = [
    path('get/products/', views.getProducts, name='index'),
    path('post/products/', views.postProducts, name='post'),
    path('get/categories/', views.getCategories, name='get_categories'),
    path('products/<slug:slug>/',
         views.ProductAPI.as_view(), name="product_detail"),
    path('products/', views.ProductsAPI.as_view(), name='products'),
    path('channels/', views.ChannelsAPI.as_view(), name='channels'),
    path('channels/<int:pk>/', views.ChannelAPI.as_view(), name='channels_detail'),
    path('images/', views.ImageAPIView.as_view(), name='image'),
]
