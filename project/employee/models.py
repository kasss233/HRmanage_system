from django.db import models
SEX_CHOICES = [
    ('男', '男'),
    ('女', '女'),
]
class employee(models.Model):
    id =models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    sex = models.CharField(max_length=2,choices=SEX_CHOICES)
    birthday=models.DateField()
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    address=models.CharField(max_length=100)