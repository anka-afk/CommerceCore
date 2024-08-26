from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import (
    User, Category, Product, Order, OrderDetail, ShoppingCart, 
    CartItem, UserProfile, FavoriteList, FavoriteItem, 
    GoodsBrowser, Announcement, Comment
)

# 自定义 AdminSite
class MyAdminSite(admin.AdminSite):
    site_header = "隙间小铺管理界面"  # 页面左上角的标题
    site_title = "隙间小铺后端管理"  # 浏览器选项卡的标题

# 实例化自定义的 AdminSite
my_admin_site = MyAdminSite(name='myadmin')



# 自定义用户创建表单
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# 自定义用户编辑表单
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        return self.initial["password"]

# 自定义 UserAdmin
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

# 使用自定义的 AdminSite 注册模型
my_admin_site.register(User, UserAdmin)
my_admin_site.register(Category)
my_admin_site.register(Product)
my_admin_site.register(Order)
my_admin_site.register(OrderDetail)
my_admin_site.register(ShoppingCart)
my_admin_site.register(CartItem)
my_admin_site.register(UserProfile)
my_admin_site.register(FavoriteList)
my_admin_site.register(FavoriteItem)
my_admin_site.register(Announcement)
my_admin_site.register(GoodsBrowser)
my_admin_site.register(Comment)

# 更新 urls.py 中的配置
# 在你的 urls.py 中，确保使用 my_admin_site
# from .admin import my_admin_site
# urlpatterns = [
#     path('admin/', my_admin_site.urls),
#     # 其他路径...
# ]
