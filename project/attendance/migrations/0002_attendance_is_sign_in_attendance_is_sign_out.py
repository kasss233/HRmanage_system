# Generated by Django 5.1.4 on 2024-12-17 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="is_sign_in",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="attendance",
            name="is_sign_out",
            field=models.BooleanField(default=False),
        ),
    ]
