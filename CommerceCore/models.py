from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(verbose_name = "商品名称",max_length=100)
    image = models.CharField(verbose_name = "商品图片",upload_to='')
    click = models.IntegerField(verbose_name = "点击量")
    unit = models.CharField(verbose_name = "单位重量",max_length = 20,default = "500g")
    description = models.TextField(verbose_name = "商品描述")
    details = models.TextField(verbose_name = "商品详情")
    price = models.DecimalField(verbose_name = "价格",max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(verbose_name = "库存数量")
    category = models.ForeignKey(Category, verbose_name = "类别id",on_delete=models.CASCADE)
    listing_date = models.DateTimeField(verbose_name = "上架时间",auto_now_add=True)
    suggest = models.BooleanField(verbose_name = "推荐",default = False)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for Order {self.order.id}"

class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"CartItem {self.id} in Cart {self.cart.id}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"
