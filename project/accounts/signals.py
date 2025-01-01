from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from employee.models import employee

@receiver(post_migrate)
def create_manager(sender, **kwargs):
    group_names = ['employee', 'group_leader', 'department_manager', 'general_manager']
    for group_name in group_names:
        if not Group.objects.filter(name=group_name).exists():
            Group.objects.create(name=group_name)
    if not User.objects.filter(username='1').exists():
        # 创建总经理账号
        user = User.objects.create(
            username='1',
            password=make_password('1')  # 总经理的密码设为 '1'，可以修改
        )
        
        # 创建员工信息
        emp = employee.objects.create(
            id=1,
            name="总经理",
            sex="男",
            birthday="1980-01-01",
            email="manager@example.com",
            phone="1234567890",
            address="总部地址",
            department="管理部",
            position="总经理",
            user=user
        )
        
        # 将总经理用户添加到总经理组
        employee_group = Group.objects.get(name='general_manager')
        user.groups.add(employee_group)
