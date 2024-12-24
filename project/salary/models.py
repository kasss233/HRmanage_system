from django.db import models
<<<<<<< HEAD
from attendance.models import Attendance
from datetime import datetime, timedelta
=======

>>>>>>> 29db69bdcee67c93b3434565e9ef4f2c3d1b0220

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
<<<<<<< HEAD
        if self.level is not None:
            try:
                # 获取对应的 SalaryStandard 对象
                salary_standard = SalaryStandard.objects.get(standard_no=self.level)
=======
        # 确保 level、bonus 和 basic_salary 都不是 None
        if self.level is not None:
            try:
                # 获取对应的 SalaryStandard 对象
                salary_standard = SalaryStandard.objects.get(id=self.level)
>>>>>>> 29db69bdcee67c93b3434565e9ef4f2c3d1b0220

                # 处理 None 值，避免加法操作中的错误
                bonus = self.bonus if self.bonus is not None else 0  # 如果 bonus 为 None, 视为 0
                basic_salary = salary_standard.basic_salary if salary_standard.basic_salary is not None else 0  # 如果 basic_salary 为 None, 视为 0

<<<<<<< HEAD
                # 获取迟到和缺勤次数
                late_count = Attendance.get_late_count(self.id)  # 使用类方法获取迟到次数
                early_count = Attendance.get_early_count(self.id)
                absence_count = Attendance.get_absent_count(self.id)  # 使用类方法获取缺勤次数

                # 获取迟到和缺勤的扣款
                late_deduction = late_count * salary_standard.late_deduction if salary_standard.late_deduction else 0
                early_deduction = early_count * salary_standard.late_deduction if salary_standard.late_deduction else 0
                absence_deduction = absence_count * salary_standard.absence_deduction if salary_standard.absence_deduction else 0

                # 计算 total_salary: 基本工资 + 奖金 - 迟到扣除 - 缺勤扣除
                self.total_salary = basic_salary + bonus - late_deduction - early_deduction - absence_deduction
                # print("late_deduction: ", late_deduction, "early_deduction: ", early_deduction, "absence_deduction: ", absence_deduction, "bonus: ", bonus, "basic_salary: ", basic_salary, "total_salary: ", self.total_salary)
            except SalaryStandard.DoesNotExist:
                # 如果没有找到对应的 SalaryStandard，设置 total_salary 为奖金
                self.total_salary = self.bonus if self.bonus is not None else 0

        super().save(*args, **kwargs)



=======
                # 计算 total_salary
                self.total_salary = basic_salary + bonus

            except SalaryStandard.DoesNotExist:
                # 如果没有找到对应的 SalaryStandard，设置 total_salary 为 bonus
                self.total_salary = self.bonus if self.bonus is not None else 0

        # 确保 bonus 也不是 None，默认值为 0
        elif self.bonus is not None:
            self.total_salary = self.bonus

        super().save(*args, **kwargs)

>>>>>>> 29db69bdcee67c93b3434565e9ef4f2c3d1b0220
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
