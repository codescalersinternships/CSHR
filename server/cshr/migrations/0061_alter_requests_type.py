# Generated by Django 4.1.2 on 2022-10-23 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0060_hrletters_with_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="requests",
            name="type",
            field=models.CharField(
                choices=[
                    ("hr_letters", "HR Letters"),
                    ("compensations", "Compensations"),
                    ("vacations", "Vacations"),
                ],
                max_length=20,
            ),
        ),
    ]
