# Generated by Django 4.0.7 on 2022-09-11 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0031_publicholidays_alter_vacationbalance_compensation_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="VacationBalance",
        ),
    ]
