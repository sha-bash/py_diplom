from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'shops', views.ShopViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'product-info', views.ProductInfoViewSet)
router.register(r'cart', views.CartViewSet, basename='cart')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'contacts', views.ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('partner/update/', views.PartnerUpdate.as_view(), name='partner-update'),
    path('order/<int:order_id>/', views.OrderDetail.as_view(), name='order-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
