"""
URL configuration for CommerceCore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomAuthToken
from .views import ShoppingCartViewSet

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
