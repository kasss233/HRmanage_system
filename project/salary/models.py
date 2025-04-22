from django.db import models
from attendance.models import Attendance
from datetime import datetime, timedelta
from decimal import Decimal 
class Salary(models.Model):
    id = models.IntegerField(primary_key=True)
    level = models.IntegerField(null=True, blank=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=[('未发', '未发'), ('已发', '已发')], default='未发')

    class Meta:
        db_table = 'salary_salary'

    def __str__(self):
        return f"Salary ID: {self.id}, Level: {self.level}"

    

    def save(self, *args, **kwargs):
        if self.level is not None:
            try:
                # 获取对应的 SalaryStandard 对象
                salary_standard = SalaryStandard.objects.get(standard_no=self.level)

                # 处理 None 值，避免加法操作中的错误
                bonus = Decimal(self.bonus) if self.bonus is not None else Decimal(0)  # 转换为 Decimal
                basic_salary = salary_standard.basic_salary if salary_standard.basic_salary is not None else Decimal(0)

                # 获取迟到和缺勤次数
                late_count = Attendance.get_late_count(self.id)
                early_count = Attendance.get_early_count(self.id)
                absence_count = Attendance.get_absent_count(self.id)

                # 获取迟到和缺勤的扣款
                late_deduction = Decimal(late_count) * salary_standard.late_deduction if salary_standard.late_deduction else Decimal(0)
                early_deduction = Decimal(early_count) * salary_standard.late_deduction if salary_standard.late_deduction else Decimal(0)
                absence_deduction = Decimal(absence_count) * salary_standard.absence_deduction if salary_standard.absence_deduction else Decimal(0)

                # 计算 total_salary: 基本工资 + 奖金 - 迟到扣除 - 缺勤扣除
                self.total_salary = basic_salary + bonus - late_deduction - early_deduction - absence_deduction
            except SalaryStandard.DoesNotExist:
                # 如果没有找到对应的 SalaryStandard，设置 total_salary 为奖金
                self.total_salary = Decimal(self.bonus) if self.bonus is not None else Decimal(0)

        super().save(*args, **kwargs)



class SalaryStandard(models.Model):
    id = models.AutoField(primary_key=True)
    standard_no = models.CharField(max_length=50)
    standard_name = models.CharField(max_length=100)
    creator = models.CharField(max_length=50)
    creation_date = models.DateField()
    registrar = models.CharField(max_length=50)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    standard_status = models.CharField(max_length=10, choices=[('有效', '有效'), ('无效', '无效')])
    late_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    absence_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    full_attendance_bonus = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'salary_standard'

    def __str__(self):
        return f"Standard Name: {self.standard_name}"
