# Generated by Django 5.1.4 on 2024-12-10 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="employee",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("sex", models.CharField(max_length=100)),
                ("birthday", models.DateField()),
                ("email", models.EmailField(max_length=100)),
                ("phone", models.IntegerField()),
                ("address", models.CharField(max_length=100)),
                ("ability", models.CharField(max_length=100)),
                ("experience", models.CharField(max_length=100)),
            ],
        ),
    ]
