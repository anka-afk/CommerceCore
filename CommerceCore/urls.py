from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import ProductViewSet, ShoppingCartViewSet, CustomAuthToken
from . import views

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', ShoppingCartViewSet, basename='cart')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('products/', views.product_list, name='product_list'),
    path('productsver2/', views.product_list_ver2, name='product_list_ver2'),
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
