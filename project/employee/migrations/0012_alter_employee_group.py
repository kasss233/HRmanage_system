# Generated by Django 5.1.4 on 2025-05-08 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0011_employee_details"),
        ("group", "0004_alter_group_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="employees",
                to="group.group",
            ),
        ),
    ]
