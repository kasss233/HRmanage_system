# Generated by Django 5.1.4 on 2024-12-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0005_alter_employee_sex"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="sex",
            field=models.CharField(choices=[("男", "男"), ("女", "女")], max_length=2),
        ),
    ]
