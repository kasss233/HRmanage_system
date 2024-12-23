from django.db import models

# Create your models here.
class employee(models.Model):
    id =models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.IntegerField()
class manager(models.Model):
    id =models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.IntegerField()
    