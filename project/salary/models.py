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
