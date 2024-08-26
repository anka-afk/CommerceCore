from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    ProductViewSet, 
    ShoppingCartViewSet,
    UserViewSet,
    CatagoryViewSet,
    RegisterView,
    CustomTokenObtainPairView,
    FavoriteListViewSet,
    FavoriteItemViewSet,
    AnnouncementViewSet,
    logout_view,
    RemoveFavoriteItemView,
    OrderCreateAPIView,
    OrderDetailAPIView,
    OrderListView,
    CommentViewSet,
    GoodsBrowserViewSet,
    mysql_shell
)
from django.views.static import serve as static_serve
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', ShoppingCartViewSet, basename='cart')
router.register(r'user', UserViewSet, basename='user')
router.register(r'categories', CatagoryViewSet)
router.register(r'favorites', FavoriteListViewSet, basename='favorite_list')
router.register(r'favorite-items', FavoriteItemViewSet, basename='favorite-item')
router.register(r'announcements', AnnouncementViewSet)
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'browsing-history', GoodsBrowserViewSet, basename='browsing-history')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('products/', views.product_list, name='product_list'),
    path('productsver2/', views.product_list_ver2, name='product_list_ver2'),
    path('', views.home, name='home'),
    path('api/', include(router.urls)),  # 确保正确注册 API 路由
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', logout_view, name='api_logout'),
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    path('api/favorite-items/remove/', RemoveFavoriteItemView.as_view(), name='remove_favorite_item'),
    path('api/orders/create/', OrderCreateAPIView.as_view(), name='order_create'),
    path('api/orders/<int:number>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('api/orders/', OrderListView.as_view(), name='order_list'),
    path('api/mysql-shell/', mysql_shell, name='mysql_shell'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
