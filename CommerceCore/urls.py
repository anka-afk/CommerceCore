from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductViewSet, ShoppingCartViewSet,UserViewSet,CatagoryViewSet,RegisterView,CustomTokenObtainPairView,FavoriteListViewSet, FavoriteItemViewSet,AnnouncementViewSet,logout_view
from . import views
from django.views.static import serve as static_serve
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', ShoppingCartViewSet, basename='cart')
router.register(r'user', UserViewSet, basename='user')
router.register(r'categories', CatagoryViewSet)
router.register(r'favorites', FavoriteListViewSet, basename='favorite_list')
router.register(r'favorite-items', FavoriteItemViewSet, basename='favorite_item')
router.register(r'announcements', AnnouncementViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('products/', views.product_list, name='product_list'),
    path('productsver2/', views.product_list_ver2, name='product_list_ver2'),
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', logout_view, name='api_logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

