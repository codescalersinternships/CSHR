# Generated by Django 4.0.7 on 2022-09-26 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0049_office_official_holidays_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vacationbalance",
            name="public_holidays",
            field=models.IntegerField(),
        ),
    ]
