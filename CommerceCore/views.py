from django.shortcuts import render
from .models import Product,ShoppingCart,Order,OrderDetail,Payment,CartItem
from rest_framework import viewsets,serializers
from .serializers import ProductSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

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
        items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({'status': 'item added'})

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')

        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()

        return Response({'status': 'item removed'})