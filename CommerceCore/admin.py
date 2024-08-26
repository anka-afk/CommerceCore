from django.contrib import admin
from .models import User, Category, Product, Order, OrderDetail, ShoppingCart, CartItem,UserProfile,FavoriteList, FavoriteItem,GoodsBrowser,Announcement,Comment
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(ShoppingCart)
admin.site.register(CartItem)
admin.site.register(UserProfile)
admin.site.register(FavoriteList)
admin.site.register(FavoriteItem)
admin.site.register(Announcement)
admin.site.register(GoodsBrowser)
admin.site.register(Comment)

# 取消默认的 User 注册
admin.site.unregister(User)

# 自定义用户创建表单，确保密码正确加密
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # 确保两次输入的密码一致
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # 确保密码经过加密后存储
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# 自定义用户编辑表单，确保显示和编辑时正确处理密码
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # 无论用户是否更新密码，都返回初始值
        return self.initial["password"]

# 自定义UserAdmin，将自定义的表单类集成
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

# 重新注册 User 模型和自定义的 UserAdmin
admin.site.register(User, UserAdmin)