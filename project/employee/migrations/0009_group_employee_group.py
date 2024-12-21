# Generated by Django 5.1.4 on 2024-12-19 14:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_employee_department_employee_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='group',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leader_of_group', to='employee.employee')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='employee.group'),
        ),
    ]
