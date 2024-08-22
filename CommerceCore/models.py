from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="用户名称", max_length=50, unique=True, blank=False)
    sex = models.CharField(verbose_name="性别", max_length=10, blank=True)
    password = models.CharField(verbose_name="密码", max_length=255, blank=False)
    email = models.EmailField(verbose_name="邮箱", unique=True, blank=True)
    phone_number = models.CharField(verbose_name="电话号码", max_length=20, blank=False)
    tel = models.CharField(verbose_name="联系方式", max_length=20, blank=True)
    address = models.CharField(verbose_name="地址", max_length=255, blank=True, default="")
    registration_date = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # 可以改为 'email' 如果你想用邮箱作为登录标识符
    REQUIRED_FIELDS = ['email']  # 必填字段，除了 USERNAME_FIELD

    def __str__(self):
        return self.username

class Category(models.Model):
    category_name = models.CharField(verbose_name="分类名称", max_length=100)
    description = models.TextField(verbose_name="分类描述", blank=True)
    image = models.ImageField(verbose_name="分类图片", upload_to='category_images/', default='category_images/default.jpg')
    
    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(verbose_name="商品ID", primary_key=True)
    product_name = models.CharField(verbose_name="商品名称", max_length=100)
    image = models.ImageField(verbose_name="商品图片", upload_to='product_images/', default='category_images/default.jpg')
    click = models.IntegerField(verbose_name="点击量", default=0)
    unit = models.CharField(verbose_name="单位重量", max_length=20, default="500g")
    description = models.TextField(verbose_name="商品描述", blank=True)
    details = models.TextField(verbose_name="商品详情", blank=True)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(verbose_name="库存数量")
    category = models.ForeignKey(Category, verbose_name="类别", on_delete=models.CASCADE)
    listing_date = models.DateTimeField(verbose_name="上架时间", auto_now_add=True)
    suggest = models.BooleanField(verbose_name="推荐", default=False)

    def __str__(self):
        return self.product_name



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    order_date = models.DateTimeField(verbose_name="订单时间", auto_now_add=True)
    total_amount = models.DecimalField(verbose_name="总金额", max_digits=10, decimal_places=2)
    order_status = models.CharField(verbose_name="订单状态", max_length=50)
    pay = models.BooleanField(verbose_name="支付", default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品", to_field='product_id')
    quantity = models.IntegerField(verbose_name="数量")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总价", default=0)
    address = models.CharField(max_length=255, verbose_name="地址", blank=True, default="")

    def __str__(self):
        return f"Detail for Order {self.order.id}"

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

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    payment_method = models.CharField(max_length=50, verbose_name="支付方式")
    payment_status = models.CharField(max_length=50, verbose_name="支付状态")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="支付时间")

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"

class GoodsBrowser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品", to_field='product_id')
    browse_date = models.DateTimeField(auto_now_add=True, verbose_name="浏览时间")

    def __str__(self):
        return f"{self.user.username} browsed {self.product.product_name}"