from django.shortcuts import render
from .models import Product,ShoppingCart,Order,OrderDetail,Category,CartItem,User,UserProfile,FavoriteList, FavoriteItem,Announcement
from rest_framework import viewsets,serializers
from .serializers import ProductSerializer,ShoppingCartSerializer, CartItemSerializer,UserSerializer,CategorySerializer,RegisterSerializer,FavoriteListSerializer, FavoriteItemSerializer,AnnouncementSerializer,ProductDetailSerializer
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
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny

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

        
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']  # 支持根据分类进行筛选
    search_fields = ['product_name', 'description']  # 支持搜索商品名称和描述

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

class CatagoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def retrieve(self, request, pk=None):
        user = request.user  # 使用 request.user 获取当前用户
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = request.user  # 使用 request.user 获取当前用户
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'patch'], url_path='profile')
    def profile(self, request):
        user = request.user
        if request.method == 'PATCH':
            # 创建 request.data 的可变副本
            mutable_data = request.data.copy()

            # 更新用户信息
            serializer = UserSerializer(user, data=mutable_data, partial=True)
            if serializer.is_valid():
                serializer.save()

                # 处理头像更新
                if 'avatar' in request.FILES:
                    user.profile.avatar = request.FILES['avatar']
                    user.profile.save()

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(user)
            return Response(serializer.data)
    @action(detail=False, methods=['post'], url_path='upload-avatar')
    def upload_avatar(self, request):
        user = request.user
        if 'avatar' in request.data:
            user.profile.avatar = request.data['avatar']
            user.profile.save()
            return Response({'avatar': user.profile.avatar.url}, status=status.HTTP_200_OK)
        return Response({'error': 'Avatar file not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='delete-account')
    def delete_account(self, request):
        user = request.user
        password = request.data.get('password')
        if not user.check_password(password):
            return Response({'error': 'Password incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return Response({'status': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print("Incoming data:", request.data)  # 打印请求数据
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "注册成功"}, status=status.HTTP_201_CREATED)
        print("Validation errors:", serializer.errors)  # 打印验证错误
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class FavoriteListViewSet(viewsets.ModelViewSet):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteList.objects.filter(user=self.request.user)

class FavoriteItemViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        favorite_list = FavoriteList.objects.get(user=self.request.user)
        return FavoriteItem.objects.filter(favorite_list=favorite_list)

    def perform_create(self, serializer):
        favorite_list, created = FavoriteList.objects.get_or_create(user=self.request.user)
        serializer.save(favorite_list=favorite_list)
        
class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    
@api_view(['POST'])
def logout_view(request):
    try:
        # 输出请求数据到日志
        print(f"Request data: {request.data}")

        # 从请求数据中获取 refresh_token
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token provided."}, status=status.HTTP_400_BAD_REQUEST)

        # 尝试创建 Token 并黑名单化
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        # 输出成功信息到日志
        print("Token successfully blacklisted.")

    except Exception as e:
        # 针对已加入黑名单的令牌，返回特定的错误信息
        if 'Token is blacklisted' in str(e):
            print("Token is already blacklisted.")
            return Response({"detail": "Token is already blacklisted."}, status=status.HTTP_200_OK)
        
        # 针对无效令牌的情况，返回特定的错误信息
        elif 'Token is invalid or expired' in str(e):
            print("Token is invalid or expired.")
            return Response({"detail": "Token is invalid or expired."}, status=status.HTTP_200_OK)

        # 输出其他错误信息到日志
        print(f"Error occurred: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # 处理登出操作
    logout(request)
    return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class ProductDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer