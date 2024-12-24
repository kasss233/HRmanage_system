from django.db import models
from django.contrib.auth.models import User
SEX_CHOICES = [
    ('男', '男'),
    ('女', '女'),
]
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
    details=models.TextField(null=True)
    group = models.ForeignKey('group.Group', on_delete=models.SET_NULL, null=True, related_name='employees')
    def __str__(self):
        return self.name