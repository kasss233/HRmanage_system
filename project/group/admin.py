from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from employee.models import employee

# 注册 Employee 模型到 admin
@admin.register(employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'sex', 'birthday', 'email', 'phone', 'address', 'department', 'position')
    search_fields = ('name', 'email', 'phone')

# 如果你需要在后台操作 User 模型，通常 User 是默认已经注册的。
# 如果需要定制 User 模型的展示，你可以这样操作：
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
