from django.db import models


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
        # 确保 level、bonus 和 basic_salary 都不是 None
        if self.level is not None:
            try:
                # 获取对应的 SalaryStandard 对象
                salary_standard = SalaryStandard.objects.get(id=self.level)

                # 处理 None 值，避免加法操作中的错误
                bonus = self.bonus if self.bonus is not None else 0  # 如果 bonus 为 None, 视为 0
                basic_salary = salary_standard.basic_salary if salary_standard.basic_salary is not None else 0  # 如果 basic_salary 为 None, 视为 0

                # 计算 total_salary
                self.total_salary = basic_salary + bonus

            except SalaryStandard.DoesNotExist:
                # 如果没有找到对应的 SalaryStandard，设置 total_salary 为 bonus
                self.total_salary = self.bonus if self.bonus is not None else 0

        # 确保 bonus 也不是 None，默认值为 0
        elif self.bonus is not None:
            self.total_salary = self.bonus

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
