from django.db import models
from django.contrib.auth.models import User
SEX_CHOICES = [
    ('男', '男'),
    ('女', '女'),
]
class group(models.Model):
    name = models.CharField(max_length=100, null=True)  # 小组名称，如 'A组', 'B组'
    department = models.CharField(max_length=100, null=True)  # 小组所属部门
    leader = models.ForeignKey('employee', on_delete=models.SET_NULL, null=True, related_name='leader_of_group')
# 创建一个默认用户
class employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    sex = models.CharField(max_length=2,choices=SEX_CHOICES)
    birthday=models.DateField()
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    department=models.CharField(max_length=100,null=True)
    position=models.CharField(max_length=100,null=True)
    group = models.ForeignKey('group', on_delete=models.CASCADE, null=True, related_name='employees')