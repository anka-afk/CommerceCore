# serializers.py
from rest_framework import serializers
from .models import Product, ShoppingCart, CartItem,User,UserProfile,Category,FavoriteItem, FavoriteList,Announcement,Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # 使用嵌套序列化器

    class Meta:
        model = Product
        fields = '__all__'
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

class ShoppingCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True)

    class Meta:
        model = ShoppingCart
        fields = ['user', 'items']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'birthdate', 'bio']


class UserSerializer(serializers.ModelSerializer):
    

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'tel', 'address', 'sex', 'profile','registration_date']

    def update(self, instance, validated_data):
        # 更新用户模型字段
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.address = validated_data.get('address', instance.address)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.save()

        # 更新用户的profile字段
        profile = instance.profile
        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.birthdate = profile_data.get('birthdate', profile.birthdate)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.save()

        return instance
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'phone_number', 'email']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被使用")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("该用户名已被使用")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        UserProfile.objects.create(user=user)
        return user

class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = FavoriteItem
        fields = ['product', 'created_at']

class FavoriteListSerializer(serializers.ModelSerializer):
    items = FavoriteItemSerializer(many=True, read_only=True)

    class Meta:
        model = FavoriteList
        fields = ['user', 'creation_date', 'items']
        
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'rating', 'created_at']

class ProductDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'