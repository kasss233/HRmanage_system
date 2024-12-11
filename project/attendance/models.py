from django.db import models
from employee.models import employee
class Attendance(models.Model):
    employee = models.ForeignKey(employee, on_delete=models.CASCADE)
    data_id=models.CharField(max_length=20)
    sign_in=models.DateTimeField()
    sign_out=models.DateTimeField()

