# models.py
from django.db import models
from employee.models import employee
DEPARTMENT_CHOICES = [
    ('技术部', '技术部'),
    ('市场部', '市场部'),
    ('人事部', '人事部'),
    ('财务部', '财务部'),
    ('行政部', '行政部'),
    ('研发部', '研发部'),
    ('销售部', '销售部'),
    ('客服部', '客服部'),
    ('运营部', '运营部'),
    ('采购部', '采购部'),
    ('售后部', '售后部'),
    ('公关部', '公关部'),
    ('战略部', '战略部'),
    ('人力资源部', '人力资源部'),
    ('法务部', '法务部'),
]
class Group(models.Model):
<<<<<<< HEAD
    name = models.CharField(max_length=100)  # 小组名称，如 'A组', 'B组'
=======
    name = models.CharField(max_length=100,unique=True)  # 小组名称，如 'A组', 'B组'
>>>>>>> 29db69bdcee67c93b3434565e9ef4f2c3d1b0220
    department = models.CharField(max_length=100, null=True, blank=True)  # 小组所属部门
    members = models.ManyToManyField('employee.employee', related_name='groups', blank=True)  # 小组成员
    leader = models.ForeignKey(
        'employee.employee',  # 假设 'employee' 是你员工模型的名称
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,  # 允许为空
        related_name='leader_of_group'
    )
    MAX_CAPACITY = 4
    def add_member(self, employee):
        # 添加成员前检查容量限制
        if self.members.count() < self.MAX_CAPACITY:
            self.members.add(employee)
        else:
            raise ValueError(f"小组'{self.name}'已达到最大容量！")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '小组'
        verbose_name_plural = '小组'
