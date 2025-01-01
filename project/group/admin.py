from django.contrib import admin
from .models import Group  # 导入 Group 模型


class GroupMemberInline(admin.TabularInline):
    model = Group.members.through  # 中介模型，用于管理 ManyToMany 关系
    extra = 1  # 初始显示 1 个空白成员行
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'leader', 'members_count']
    readonly_fields = ['name', 'department', 'leader']

    def members_count(self, obj):
        return obj.members.count()

# 注册模型和自定义的 Admin
admin.site.register(Group, GroupAdmin)