# Generated by Django 5.1.4 on 2024-12-21 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_employee_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='Group',
            new_name='group',
        ),
    ]