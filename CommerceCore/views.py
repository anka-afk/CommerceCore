from django.shortcuts import render
from .models import Product,ShoppingCart,Order,OrderDetail,Category,CartItem,User,UserProfile,FavoriteList, FavoriteItem,Announcement,Comment,GoodsBrowser
from rest_framework import viewsets,serializers
from .serializers import ProductSerializer,ShoppingCartSerializer, CartItemSerializer,UserSerializer,CategorySerializer,RegisterSerializer,FavoriteListSerializer, FavoriteItemSerializer,AnnouncementSerializer,ProductDetailSerializer,OrderSerializer,OrderDetailSerializer,CommentSerializer,GoodsBrowserSerializer
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
from rest_framework import filters,generics
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
import random
from django.db import transaction
from django.http import JsonResponse
from django.views import View
from django.conf import settings
import mysql.connector
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json


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
    serializer_class = ProductDetailSerializer  # 使用包含评论的序列化器
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']  # 支持根据分类进行筛选
    search_fields = ['product_name', 'description']  # 支持搜索商品名称和描述
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)  # 打印序列化后的数据
        return Response(serializer.data)

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
        
        # 验证用户输入的密码是否正确
        if not user.check_password(password):
            return Response({'error': '密码错误'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 删除用户及其相关联的表项
        user.delete()
        
        return Response({'status': '账号已成功注销'}, status=status.HTTP_204_NO_CONTENT)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # 注册成功后自动生成 JWT 令牌
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "注册成功",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
class FavoriteListViewSet(viewsets.ModelViewSet):
    queryset = FavoriteList.objects.all()
    serializer_class = FavoriteListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteList.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        favorite_list, created = FavoriteList.objects.get_or_create(user=self.request.user)
        serializer.save(favorite_list=favorite_list)



class RemoveFavoriteItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            favorite_list = FavoriteList.objects.get(user=request.user)
            favorite_item = FavoriteItem.objects.get(favorite_list=favorite_list, product__product_id=product_id)
            favorite_item.delete()
            return Response({'status': 'item removed'}, status=status.HTTP_200_OK)
        except FavoriteItem.DoesNotExist:
            return Response({'error': 'Item not found in favorites'}, status=status.HTTP_404_NOT_FOUND)

class FavoriteItemViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerializer

    def list(self, request):
        favorite_list, created = FavoriteList.objects.get_or_create(user=request.user)
        favorite_items = FavoriteItem.objects.filter(favorite_list=favorite_list)
        serializer = FavoriteItemSerializer(favorite_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='remove_from_favorites')
    def remove_from_favorites(self, request):
        product_id = request.data.get('product_id')
        try:
            favorite_list = FavoriteList.objects.get(user=request.user)
            favorite_item = FavoriteItem.objects.get(favorite_list=favorite_list, product__product_id=product_id)
            favorite_item.delete()
            return Response({'status': 'item removed'}, status=status.HTTP_200_OK)
        except FavoriteItem.DoesNotExist:
            return Response({'error': 'Item not found in favorites'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['post'], url_path='add_item')
    def add_item(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(product_id=product_id)
            favorite_list, created = FavoriteList.objects.get_or_create(user=request.user)
            favorite_item, created = FavoriteItem.objects.get_or_create(favorite_list=favorite_list, product=product)
            if created:
                return Response({'status': 'item added'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'item already in favorites'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
     


        
       
        
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

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            # 创建订单
            order_data = {
                'user': request.user,
                'total_amount': request.data['total_amount'],
                'order_status': Order.AWAITING_PAYMENT,
                'payment_method': request.data['payment_method'],
            }
            order = Order.objects.create(**order_data)

            # 创建订单详情并减少库存
            for item in request.data['items']:
                product = Product.objects.get(product_id=item['product_id'])
                
                # 检查库存是否足够
                if product.stock_quantity < item['quantity']:
                    return Response({'error': '库存不足'}, status=status.HTTP_400_BAD_REQUEST)

                # 减少库存
                product.stock_quantity -= item['quantity']
                product.save()

                OrderDetail.objects.create(
                    order=order,
                    product=product,
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    discount=item['discount'],
                    tax=0.00  # 税额如果有需要计算的地方可以自行修改
                )

            # 清空购物车
            cart = ShoppingCart.objects.get(user=request.user)
            cart.cartitem_set.all().delete()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            # 创建订单
            order_data = {
                'user': request.user,
                'total_amount': request.data['total_amount'],
                'order_status': Order.AWAITING_PAYMENT,
                'payment_method': request.data['payment_method'],
            }
            order = Order.objects.create(**order_data)

            # 创建订单详情
            for item in request.data['items']:
                product = Product.objects.get(product_id=item['product_id'])
                OrderDetail.objects.create(
                    order=order,
                    product=product,
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    discount=item['discount'],
                    tax=0.00  # 税额如果有需要计算的地方可以自行修改
                )

            # 清空购物车
            cart = ShoppingCart.objects.get(user=request.user)
            cart.cartitem_set.all().delete()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'number'

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        previous_status = order.order_status  # 保存之前的订单状态

        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # 检查订单状态是否从 AWAITING_PAYMENT 变为 PAIED
            new_status = serializer.validated_data.get('order_status')
            if previous_status == Order.AWAITING_PAYMENT and new_status == Order.PAIED:
                for detail in order.order_details.all():
                    product = detail.product
                    product.sales += detail.quantity  # 增加销量
                    product.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 返回当前登录用户的所有订单
        return Order.objects.filter(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 保存评论
        comment = serializer.save(user=self.request.user)

        # 获取相关的产品
        product = comment.product

        # 更新评分总数和评分人数
        product.rating_count += 1
        product.score_total += comment.rating  # 假设 score 是评分的总和
        
        product.score = product.score_total / product.rating_count

        # 保存产品
        product.save()

class GoodsBrowserViewSet(viewsets.ModelViewSet):
    serializer_class = GoodsBrowserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 返回当前登录用户的所有浏览记录，按浏览时间倒序排列
        return GoodsBrowser.objects.filter(user=self.request.user).order_by('-browse_date')

    @action(detail=False, methods=['post'], url_path='record')
    def record(self, request):
        product_id = request.data.get('product')
        user = request.user  # 获取当前的用户

        # 验证前端传来的产品ID
        product = get_object_or_404(Product, pk=product_id)
        
        # 增加物品的点击量
        product.click += 1
        product.save()

        # 创建浏览记录
        goods_browser = GoodsBrowser.objects.create(user=self.request.user, product=product)

        # 返回成功响应
        return Response({
            'status': 'Browsing history recorded successfully',
            'data': GoodsBrowserSerializer(goods_browser).data
        }, status=status.HTTP_201_CREATED)


@csrf_exempt  # 如果前端已经正确传递CSRF token，可以删除此行
@require_POST
def mysql_shell(request):
    try:
        # 解析 JSON 请求体
        data = json.loads(request.body.decode('utf-8'))
        query = data.get('query', '')
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)

    # 配置你的MySQL数据库连接
    db_config = {
        'user': 'root',          # MySQL用户名
        'password': '555555',    # MySQL密码
        'host': 'localhost',     # 数据库主机
        'database': 'commercecore',  # 数据库名称
    }

    connection = None
    cursor = None
    try:
        # 连接到数据库
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(query)
        
        # 检查是否有返回数据
        if cursor.with_rows:
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]
            result = {
                "headers": headers,
                "rows": rows,
            }
        else:
            # 没有返回数据则提交事务
            connection.commit()
            result = {"headers": [], "rows": [["Query executed successfully"]]}
    except mysql.connector.Error as err:
        # 捕获并返回MySQL错误
        return JsonResponse({"error": str(err)}, status=400)
    finally:
        # 确保只有在cursor和connection被初始化时才调用close()
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return JsonResponse(result)