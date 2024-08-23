from django.shortcuts import render
from .models import Product,ShoppingCart,Order,OrderDetail,Payment,CartItem,User
from rest_framework import viewsets,serializers
from .serializers import ProductSerializer,ShoppingCartSerializer, CartItemSerializer,UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_list_ver2(request):
    products = Product.objects.all()
    return render(request, 'product_list_ver2.html', {'products': products})

def home(request):
    featured_products = Product.objects.filter(suggest=True)[:4]
    new_arrivals = Product.objects.order_by('-listing_date')[:4]
    return render(request, 'index.html', {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals
    })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.product_name')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity']

class ShoppingCartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        serializer = ShoppingCartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(product_id=product_id)
            cart, created = ShoppingCart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            return Response({'status': 'item added'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        product_id = request.data.get('product_id')
        try:
            cart = ShoppingCart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product__product_id=product_id)
            cart_item.delete()
            return Response({'status': 'item removed'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def update_quantity(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            cart = ShoppingCart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product__product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
            return Response({'status': 'quantity updated'}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)
        
class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get', 'patch'], url_path='profile')
    def profile(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(user)
            return Response(serializer.data)