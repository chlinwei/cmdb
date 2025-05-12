from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')  # 控制列表页字段显示
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('角色信息', {'fields': ('role',)}),  # 新增的role字段分组
        ('权限信息', {'fields': ('is_active', 'is_staff', 'groups')}),
    )