# serializers.py
from rest_framework import serializers
from .models import Product, ShoppingCart, CartItem,User,UserProfile,Category

class ProductSerializer(serializers.ModelSerializer):
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
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'description', 'image']

class UserSerializer(serializers.ModelSerializer):
    

    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'tel', 'address', 'sex', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.address = validated_data.get('address', instance.address)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.save()

        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.birthdate = profile_data.get('birthdate', profile.birthdate)
        profile.bio = profile_data.get('bio', profile.bio)
        profile.save()

        return instance