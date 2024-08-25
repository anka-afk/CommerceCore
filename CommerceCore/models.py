from django.db import models,transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,User
import datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名必须填写')
        email = self.normalize_email(email)
        
        with transaction.atomic():  # 保持事务原子性，确保所有操作同时成功或失败
            user = self.model(username=username, email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            # 创建关联的 UserProfile, ShoppingCart, FavoriteList
            UserProfile.objects.create(user=user)
            ShoppingCart.objects.create(user=user)
            FavoriteList.objects.create(user=user)

        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须有is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须有is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="用户名称", max_length=50, unique=True, blank=False)
    sex = models.CharField(verbose_name="性别", max_length=10, blank=True,default = "未填写")
    password = models.CharField(verbose_name="密码", max_length=255, blank=False)
    email = models.EmailField(verbose_name="邮箱", unique=True, blank=True)
    phone_number = models.CharField(verbose_name="电话号码", max_length=20, blank=False,default = "未填写")
    tel = models.CharField(verbose_name="联系方式", max_length=20, blank=True,default = "未填写")
    address = models.CharField(verbose_name="地址", max_length=255, blank=True, default = "未填写")
    registration_date = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # 可以改为 'email' 如果你想用邮箱作为登录标识符
    REQUIRED_FIELDS = ['email']  # 必填字段，除了 USERNAME_FIELD

    def __str__(self):
        return self.username

    # 在删除用户时，自动删除相关联的表项
    def delete(self, *args, **kwargs):
        # 在删除用户之前，检查相关对象是否存在
        try:
            if hasattr(self, 'profile'):
                self.profile.delete()  # 删除 UserProfile
        except ObjectDoesNotExist:
            pass  # 如果对象不存在，忽略异常

        try:
            if hasattr(self, 'shoppingcart'):
                self.shoppingcart.delete()  # 删除 ShoppingCart
        except ObjectDoesNotExist:
            pass

        try:
            if hasattr(self, 'favoritelist'):
                self.favoritelist.delete()  # 删除 FavoriteList
        except ObjectDoesNotExist:
            pass

        # 调用父类的删除方法
        super().delete(*args, **kwargs)

class Category(models.Model):
    category_name = models.CharField(verbose_name="分类名称", max_length=100)
    description = models.TextField(verbose_name="分类描述", blank=True)
    image = models.ImageField(verbose_name="分类图片", upload_to='category_images/', default='avatars/default.png')
    
    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(verbose_name="商品ID", primary_key=True)
    product_name = models.CharField(verbose_name="商品名称", max_length=100,default="Unnamed Product")
    image = models.ImageField(verbose_name="商品图片", upload_to='product_images/', default='avatars/default.png')
    click = models.IntegerField(verbose_name="点击量", default=0)
    unit = models.CharField(verbose_name="单位", max_length=20, default="个")
    description = models.TextField(verbose_name="商品描述", blank=True)
    details = models.TextField(verbose_name="商品详情", blank=True)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(verbose_name="库存数量")
    category = models.ForeignKey(Category, verbose_name="类别", on_delete=models.CASCADE,related_name="products")
    listing_date = models.DateTimeField(verbose_name="上架时间", auto_now_add=True)
    suggest = models.BooleanField(verbose_name="推荐", default=False)
    score = models.IntegerField(verbose_name="评分", default=0)
    sales = models.IntegerField(verbose_name="销量", default=0)
    rating_count = models.IntegerField(verbose_name="评分人数", default=0)
    def __str__(self):
        return self.product_name

class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="评论内容")
    rating = models.IntegerField(verbose_name="评分", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} - {self.rating}星"
class Order(models.Model):
    # 状态名称及描述
    SHIPPED = 'shipped'  # 已发货
    OUT_FOR_DELIVERY = 'out_for_delivery'  # 派送中
    DELIVERED = 'delivered'  # 已送达
    CANCELLED = 'cancelled'  # 已取消
    AWAITING_PAYMENT = 'awaiting_payment'  # 等待支付
    PAYMENT_FAILED = 'payment_failed'  # 支付失败
    REFUNDED = 'refunded'  # 已退款
    PAIED = 'paied'  # 已支付

    ORDER_STATUS_CHOICES = [
        (AWAITING_PAYMENT, 'Awaiting Payment'),
        (PAYMENT_FAILED, 'Payment Failed'),
        (SHIPPED, 'Shipped'),
        (OUT_FOR_DELIVERY, 'Out for Delivery'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
        (REFUNDED, 'Refunded'),
        (PAIED, 'Paied')
    ]

    number = models.BigAutoField(primary_key=True, verbose_name="订单号")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    order_date = models.DateTimeField(verbose_name="订单时间", auto_now_add=True)
    total_amount = models.DecimalField(verbose_name="总金额", max_digits=10, decimal_places=2)
    order_status = models.CharField(verbose_name="订单状态", max_length=20, choices=ORDER_STATUS_CHOICES, default=AWAITING_PAYMENT)
    payment_method = models.CharField(max_length=50, verbose_name="支付方式", blank=True, default="")

    def __str__(self):
        return f"Order {self.number} by {self.user.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单", related_name="order_details")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    product_name = models.CharField(verbose_name="商品名称", max_length=100,default="Unnamed Product")  # 记录下商品的名称
    quantity = models.IntegerField(verbose_name="数量")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="折扣", default=0.00)  # 商品折扣
    tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="税额", default=0.00)  # 商品税额
    
    @property
    def total_price(self):
        return (self.unit_price - self.discount) * self.quantity + self.tax

    def __str__(self):
        return f"Detail for Order {self.order.number} - Product {self.product.product_name}"


class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, verbose_name="购物车")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品", to_field='product_id')
    quantity = models.IntegerField(verbose_name="数量", default=1)

    def __str__(self):
        return f"CartItem {self.id} in Cart {self.cart.id}"

class GoodsBrowser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品", to_field='product_id')
    browse_date = models.DateTimeField(auto_now_add=True, verbose_name="浏览时间")

    def __str__(self):
        return f"{self.user.username} browsed {self.product.product_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', verbose_name="头像")
    birthdate = models.DateField(null=True, blank=True, verbose_name="生日",default=datetime.date(2000, 1, 1))
    bio = models.TextField(blank=True, verbose_name="个人简介",default = "未填写")

    def __str__(self):
        return f"{self.user.username}'s profile"

class FavoriteList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return f"FavoriteList for {self.user.username}"

class FavoriteItem(models.Model):
    favorite_list = models.ForeignKey(FavoriteList, on_delete=models.CASCADE, verbose_name="收藏列表")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name="商品")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    def __str__(self):
        return f"FavoriteItem {self.product.product_name} in FavoriteList {self.favorite_list.id}"

class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.title