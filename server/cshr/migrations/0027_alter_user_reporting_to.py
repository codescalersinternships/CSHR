# Generated by Django 4.0.7 on 2022-09-11 11:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0026_remove_user_reporting_to_user_reporting_to"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="reporting_to",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
