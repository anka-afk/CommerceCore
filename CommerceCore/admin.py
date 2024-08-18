from django.contrib import admin
from .models import User, Category, Product, Order, OrderDetail, ShoppingCart, CartItem, Payment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(Payment)
