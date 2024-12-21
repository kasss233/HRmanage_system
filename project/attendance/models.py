from django.db import models
from employee.models import employee
class Attendance(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    date=models.DateField(null=True)
    sign_in=models.DateTimeField(null=True)
    sign_out=models.DateTimeField(null=True)
    is_sign_in=models.BooleanField(default=False)
    is_sign_out=models.BooleanField(default=False)
    remarks=models.TextField(null=True)
