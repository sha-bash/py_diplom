from django.urls import path
from . import views

urlpatterns = [
    path('shops/', views.ShopList.as_view(), name='shop-list'),
    path('shops/<int:pk>/', views.ShopDetail.as_view(), name='shop-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('product-info/', views.ProductInfoList.as_view(), name='productinfo-list'),
    path('product-info/<int:pk>/', views.ProductInfoDetail.as_view(), name='productinfo-detail'),
]
