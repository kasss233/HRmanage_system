# models.py
from django.db import models
from employee.models import employee

class Group(models.Model):
    name = models.CharField(max_length=100, blank=True,primary_key=True)  # 小组名称，如 'A组', 'B组'
    department = models.CharField(max_length=100, null=True, blank=True)  # 小组所属部门
    members = models.ManyToManyField(employee, related_name='groups', blank=True)  # 小组成员
    leader = models.ForeignKey(
        'employee.Employee',  # 假设 'employee' 是你员工模型的名称
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
